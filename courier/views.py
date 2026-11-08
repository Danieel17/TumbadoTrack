from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from .models import Cliente, Conductor, Envio, Producto, Proveedor, Vehiculo
from .reportes import ejecutar_consultas


def _es_administrador(user):
    """Un administrador es un usuario autenticado con is_staff=True."""
    return user.is_authenticated and user.is_staff


# Decorador reutilizable: exige sesión iniciada Y rol de administrador.
# Si no está autenticado, redirige a LOGIN_URL (configurado en settings.py);
# si está autenticado pero no es staff, Django responde con permiso denegado.
admin_requerido = user_passes_test(_es_administrador, login_url="courier:login")


def landing(request):
    """Página promocional pública, previa al login: qué es TumbadoTrack y qué resuelve."""
    if request.user.is_authenticated:
        return redirect("courier:dashboard")
    return render(request, "courier/landing.html")


def login_view(request):
    """Login real contra el modelo de usuarios de Django (auth)."""
    if request.user.is_authenticated:
        return redirect("courier:dashboard")

    error = None
    if request.method == "POST":
        usuario = request.POST.get("usuario", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=usuario, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect("courier:dashboard")
        error = "Usuario o contraseña incorrectos."

    return render(request, "courier/login.html", {"error": error})


def logout_view(request):
    """El cierre de sesión solo se procesa por POST (nunca por un link/GET),
    para que una imagen o un link malicioso no pueda cerrar la sesión de
    alguien sin que lo sepa."""
    if request.method == "POST":
        logout(request)
    return redirect("courier:landing")


@login_required(login_url="courier:login")
def dashboard(request):
    """Vista principal: estadísticas generales del sistema de courier."""
    contexto = {
        "estadisticas": {
            "total_envios": Envio.objects.count(),
            "en_transito": Envio.objects.filter(estado=Envio.ESTADO_EN_TRANSITO).count(),
            "en_aduana": Envio.objects.filter(estado=Envio.ESTADO_EN_ADUANA).count(),
            "entregados": Envio.objects.filter(estado=Envio.ESTADO_ENTREGADO).count(),
            "preparando": Envio.objects.filter(estado=Envio.ESTADO_PREPARANDO).count(),
            "total_proveedores": Proveedor.objects.count(),
            "total_clientes": Cliente.objects.count(),
        },
        "envios_recientes": Envio.objects.select_related("producto", "proveedor", "cliente")[:5],
    }
    return render(request, "courier/dashboard.html", contexto)


@login_required(login_url="courier:login")
def lista_envios(request):
    """Listado de todos los envíos, con sus relaciones ya resueltas."""
    estado_filtro = request.GET.get("estado")

    envios = Envio.objects.select_related("producto", "proveedor", "cliente")
    if estado_filtro:
        envios = envios.filter(estado=estado_filtro)

    contexto = {
        "envios": envios,
        "estado_filtro": estado_filtro,
    }
    return render(request, "courier/lista_envios.html", contexto)


@login_required(login_url="courier:login")
def detalle_envio(request, envio_id):
    """Detalle y tracking de un envío específico, con su historial de eventos."""
    envio = get_object_or_404(
        Envio.objects.select_related("producto", "proveedor", "cliente"), pk=envio_id
    )

    contexto = {
        "envio": envio,
        "eventos": envio.eventos.all(),
    }
    return render(request, "courier/detalle_envio.html", contexto)


def _opciones_envio():
    """Datos que necesita el formulario de Envío para armar los <select>."""
    return {
        "productos": Producto.objects.all(),
        "proveedores": Proveedor.objects.all(),
        "clientes": Cliente.objects.all(),
        "vehiculos": Vehiculo.objects.all(),
        "conductores": Conductor.objects.all(),
        "estados": Envio.ESTADO_CHOICES,
    }


def _leer_datos_envio(request):
    """Lee y valida a mano los campos del formulario HTML de Envío (sin ModelForm)."""
    datos = {
        "codigo": request.POST.get("codigo", "").strip(),
        "producto_id": request.POST.get("producto", ""),
        "proveedor_id": request.POST.get("proveedor", ""),
        "cliente_id": request.POST.get("cliente", ""),
        "vehiculo_id": request.POST.get("vehiculo", ""),
        "conductor_id": request.POST.get("conductor", ""),
        "origen": request.POST.get("origen", "").strip(),
        "destino": request.POST.get("destino", "").strip(),
        "peso_total_kg": request.POST.get("peso_total_kg", "").strip(),
        "estado": request.POST.get("estado", Envio.ESTADO_PREPARANDO),
        "fecha_envio": request.POST.get("fecha_envio", "").strip(),
        "fecha_estimada_entrega": request.POST.get("fecha_estimada_entrega", "").strip(),
        "fecha_real_entrega": request.POST.get("fecha_real_entrega", "").strip(),
        "ubicacion_actual": request.POST.get("ubicacion_actual", "").strip(),
        "observaciones": request.POST.get("observaciones", "").strip(),
    }

    errores = {}
    if not datos["codigo"]:
        errores["codigo"] = "El código es obligatorio."
    if not datos["producto_id"]:
        errores["producto_id"] = "Selecciona un producto."
    if not datos["proveedor_id"]:
        errores["proveedor_id"] = "Selecciona un proveedor."
    if not datos["cliente_id"]:
        errores["cliente_id"] = "Selecciona un cliente."
    if not datos["destino"]:
        errores["destino"] = "El destino es obligatorio."
    if not datos["fecha_envio"]:
        errores["fecha_envio"] = "La fecha de envío es obligatoria."
    if not datos["fecha_estimada_entrega"]:
        errores["fecha_estimada_entrega"] = "La fecha estimada de entrega es obligatoria."
    if not datos["ubicacion_actual"]:
        errores["ubicacion_actual"] = "La ubicación actual es obligatoria."
    try:
        datos["peso_total_kg"] = float(datos["peso_total_kg"])
    except ValueError:
        errores["peso_total_kg"] = "Ingresa un peso válido."

    return datos, errores


@admin_requerido
def crear_envio(request):
    errores = {}
    datos = {}

    if request.method == "POST":
        datos, errores = _leer_datos_envio(request)

        if not errores:
            Envio.objects.create(
                codigo=datos["codigo"],
                producto_id=datos["producto_id"],
                proveedor_id=datos["proveedor_id"],
                cliente_id=datos["cliente_id"],
                vehiculo_id=datos["vehiculo_id"] or None,
                conductor_id=datos["conductor_id"] or None,
                origen=datos["origen"],
                destino=datos["destino"],
                peso_total_kg=datos["peso_total_kg"],
                estado=datos["estado"],
                fecha_envio=datos["fecha_envio"],
                fecha_estimada_entrega=datos["fecha_estimada_entrega"],
                fecha_real_entrega=datos["fecha_real_entrega"] or None,
                ubicacion_actual=datos["ubicacion_actual"],
                observaciones=datos["observaciones"],
            )
            messages.success(request, "Envío creado correctamente.")
            return redirect("courier:lista_envios")

    contexto = {"titulo": "Nuevo envío", "datos": datos, "errores": errores, **_opciones_envio()}
    return render(request, "courier/envio_form.html", contexto)


@admin_requerido
def editar_envio(request, envio_id):
    envio = get_object_or_404(Envio, pk=envio_id)
    errores = {}

    if request.method == "POST":
        datos, errores = _leer_datos_envio(request)

        if not errores:
            envio.codigo = datos["codigo"]
            envio.producto_id = datos["producto_id"]
            envio.proveedor_id = datos["proveedor_id"]
            envio.cliente_id = datos["cliente_id"]
            envio.vehiculo_id = datos["vehiculo_id"] or None
            envio.conductor_id = datos["conductor_id"] or None
            envio.origen = datos["origen"]
            envio.destino = datos["destino"]
            envio.peso_total_kg = datos["peso_total_kg"]
            envio.estado = datos["estado"]
            envio.fecha_envio = datos["fecha_envio"]
            envio.fecha_estimada_entrega = datos["fecha_estimada_entrega"]
            envio.fecha_real_entrega = datos["fecha_real_entrega"] or None
            envio.ubicacion_actual = datos["ubicacion_actual"]
            envio.observaciones = datos["observaciones"]
            envio.save()
            messages.success(request, "Envío actualizado correctamente.")
            return redirect("courier:detalle_envio", envio_id=envio.id)
    else:
        datos = {
            "codigo": envio.codigo,
            "producto_id": envio.producto_id,
            "proveedor_id": envio.proveedor_id,
            "cliente_id": envio.cliente_id,
            "vehiculo_id": envio.vehiculo_id,
            "conductor_id": envio.conductor_id,
            "origen": envio.origen,
            "destino": envio.destino,
            "peso_total_kg": envio.peso_total_kg,
            "estado": envio.estado,
            "fecha_envio": envio.fecha_envio.isoformat() if envio.fecha_envio else "",
            "fecha_estimada_entrega": envio.fecha_estimada_entrega.isoformat() if envio.fecha_estimada_entrega else "",
            "fecha_real_entrega": envio.fecha_real_entrega.isoformat() if envio.fecha_real_entrega else "",
            "ubicacion_actual": envio.ubicacion_actual,
            "observaciones": envio.observaciones,
        }

    contexto = {
        "titulo": f"Editar envío · {envio.codigo}", "datos": datos, "errores": errores,
        "envio": envio, **_opciones_envio(),
    }
    return render(request, "courier/envio_form.html", contexto)


@admin_requerido
def eliminar_envio(request, envio_id):
    envio = get_object_or_404(Envio, pk=envio_id)

    if request.method == "POST":
        envio.delete()
        messages.success(request, "Envío eliminado correctamente.")
        return redirect("courier:lista_envios")

    return render(request, "courier/confirmar_eliminar.html", {
        "objeto": envio, "volver_url": "courier:detalle_envio", "volver_args": [envio.id],
    })


@login_required(login_url="courier:login")
def lista_proveedores(request):
    """Listado de proveedores de equipos musicales."""
    contexto = {"proveedores": Proveedor.objects.all()}
    return render(request, "courier/lista_proveedores.html", contexto)


def _leer_datos_proveedor(request):
    datos = {
        "nombre": request.POST.get("nombre", "").strip(),
        "pais": request.POST.get("pais", "").strip(),
        "email_contacto": request.POST.get("email_contacto", "").strip(),
        "telefono": request.POST.get("telefono", "").strip(),
        "tasa_puntualidad": request.POST.get("tasa_puntualidad", "").strip(),
        "activo": request.POST.get("activo") == "on",
    }

    errores = {}
    if not datos["nombre"]:
        errores["nombre"] = "El nombre es obligatorio."
    if not datos["pais"]:
        errores["pais"] = "El país es obligatorio."
    if not datos["email_contacto"]:
        errores["email_contacto"] = "El correo de contacto es obligatorio."
    if not datos["telefono"]:
        errores["telefono"] = "El teléfono es obligatorio."
    try:
        datos["tasa_puntualidad"] = float(datos["tasa_puntualidad"])
    except ValueError:
        errores["tasa_puntualidad"] = "Ingresa un número válido (ej. 95.5)."

    return datos, errores


@admin_requerido
def crear_proveedor(request):
    errores = {}
    datos = {}

    if request.method == "POST":
        datos, errores = _leer_datos_proveedor(request)
        if not errores:
            Proveedor.objects.create(**datos)
            messages.success(request, "Proveedor creado correctamente.")
            return redirect("courier:lista_proveedores")

    return render(request, "courier/proveedor_form.html", {
        "titulo": "Nuevo proveedor", "datos": datos, "errores": errores,
    })


@admin_requerido
def editar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, pk=proveedor_id)
    errores = {}

    if request.method == "POST":
        datos, errores = _leer_datos_proveedor(request)
        if not errores:
            for campo, valor in datos.items():
                setattr(proveedor, campo, valor)
            proveedor.save()
            messages.success(request, "Proveedor actualizado correctamente.")
            return redirect("courier:lista_proveedores")
    else:
        datos = {
            "nombre": proveedor.nombre, "pais": proveedor.pais,
            "email_contacto": proveedor.email_contacto, "telefono": proveedor.telefono,
            "tasa_puntualidad": proveedor.tasa_puntualidad, "activo": proveedor.activo,
        }

    return render(request, "courier/proveedor_form.html", {
        "titulo": f"Editar proveedor · {proveedor.nombre}", "datos": datos, "errores": errores,
    })


@admin_requerido
def eliminar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, pk=proveedor_id)

    if request.method == "POST":
        try:
            proveedor.delete()
            messages.success(request, "Proveedor eliminado correctamente.")
        except ProtectedError:
            messages.error(request, "No se puede eliminar: tiene envíos asociados.")
        return redirect("courier:lista_proveedores")

    return render(request, "courier/confirmar_eliminar.html", {
        "objeto": proveedor, "volver_url": "courier:lista_proveedores",
    })


@login_required(login_url="courier:login")
def lista_clientes(request):
    """Listado de clientes (recintos/venues del tour)."""
    contexto = {"clientes": Cliente.objects.all()}
    return render(request, "courier/lista_clientes.html", contexto)


def _leer_datos_cliente(request):
    datos = {
        "nombre": request.POST.get("nombre", "").strip(),
        "ciudad": request.POST.get("ciudad", "").strip(),
        "tipo": request.POST.get("tipo", Cliente.TIPO_VENUE),
        "email_contacto": request.POST.get("email_contacto", "").strip(),
        "telefono": request.POST.get("telefono", "").strip(),
    }

    errores = {}
    if not datos["nombre"]:
        errores["nombre"] = "El nombre es obligatorio."
    if not datos["ciudad"]:
        errores["ciudad"] = "La ciudad es obligatoria."
    if not datos["email_contacto"]:
        errores["email_contacto"] = "El correo de contacto es obligatorio."
    if not datos["telefono"]:
        errores["telefono"] = "El teléfono es obligatorio."

    return datos, errores


@admin_requerido
def crear_cliente(request):
    errores = {}
    datos = {}

    if request.method == "POST":
        datos, errores = _leer_datos_cliente(request)
        if not errores:
            Cliente.objects.create(**datos)
            messages.success(request, "Cliente creado correctamente.")
            return redirect("courier:lista_clientes")

    return render(request, "courier/cliente_form.html", {
        "titulo": "Nuevo cliente", "datos": datos, "errores": errores, "tipos": Cliente.TIPO_CHOICES,
    })


@admin_requerido
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    errores = {}

    if request.method == "POST":
        datos, errores = _leer_datos_cliente(request)
        if not errores:
            for campo, valor in datos.items():
                setattr(cliente, campo, valor)
            cliente.save()
            messages.success(request, "Cliente actualizado correctamente.")
            return redirect("courier:lista_clientes")
    else:
        datos = {
            "nombre": cliente.nombre, "ciudad": cliente.ciudad, "tipo": cliente.tipo,
            "email_contacto": cliente.email_contacto, "telefono": cliente.telefono,
        }

    return render(request, "courier/cliente_form.html", {
        "titulo": f"Editar cliente · {cliente.nombre}", "datos": datos, "errores": errores,
        "tipos": Cliente.TIPO_CHOICES,
    })


@admin_requerido
def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)

    if request.method == "POST":
        try:
            cliente.delete()
            messages.success(request, "Cliente eliminado correctamente.")
        except ProtectedError:
            messages.error(request, "No se puede eliminar: tiene envíos asociados.")
        return redirect("courier:lista_clientes")

    return render(request, "courier/confirmar_eliminar.html", {
        "objeto": cliente, "volver_url": "courier:lista_clientes",
    })


@login_required(login_url="courier:login")
def lista_vehiculos(request):
    """Listado de vehículos de la flota."""
    contexto = {"vehiculos": Vehiculo.objects.select_related("proveedor")}
    return render(request, "courier/lista_vehiculos.html", contexto)


def _leer_datos_vehiculo(request):
    datos = {
        "patente": request.POST.get("patente", "").strip().upper(),
        "tipo": request.POST.get("tipo", Vehiculo.TIPO_CAMION),
        "marca": request.POST.get("marca", "").strip(),
        "modelo": request.POST.get("modelo", "").strip(),
        "anio": request.POST.get("anio", "").strip(),
        "capacidad_kg": request.POST.get("capacidad_kg", "").strip(),
        "disponible": request.POST.get("disponible") == "on",
        "estado": request.POST.get("estado", Vehiculo.ESTADO_DISPONIBLE),
        "proveedor_id": request.POST.get("proveedor", ""),
    }

    errores = {}
    if not datos["patente"]:
        errores["patente"] = "La patente es obligatoria."
    if not datos["proveedor_id"]:
        errores["proveedor_id"] = "Selecciona un proveedor."
    try:
        datos["capacidad_kg"] = float(datos["capacidad_kg"])
    except ValueError:
        errores["capacidad_kg"] = "Ingresa una capacidad válida."
    if datos["anio"]:
        try:
            datos["anio"] = int(datos["anio"])
        except ValueError:
            errores["anio"] = "Ingresa un año válido."
    else:
        datos["anio"] = None

    return datos, errores


@admin_requerido
def crear_vehiculo(request):
    errores = {}
    datos = {}

    if request.method == "POST":
        datos, errores = _leer_datos_vehiculo(request)
        if not errores:
            proveedor_id = datos.pop("proveedor_id")
            Vehiculo.objects.create(proveedor_id=proveedor_id, **datos)
            messages.success(request, "Vehículo creado correctamente.")
            return redirect("courier:lista_vehiculos")

    return render(request, "courier/vehiculo_form.html", {
        "titulo": "Nuevo vehículo", "datos": datos, "errores": errores,
        "tipos": Vehiculo.TIPO_CHOICES, "estados": Vehiculo.ESTADO_CHOICES,
        "proveedores": Proveedor.objects.all(),
    })


@admin_requerido
def editar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
    errores = {}

    if request.method == "POST":
        datos, errores = _leer_datos_vehiculo(request)
        if not errores:
            proveedor_id = datos.pop("proveedor_id")
            for campo, valor in datos.items():
                setattr(vehiculo, campo, valor)
            vehiculo.proveedor_id = proveedor_id
            vehiculo.save()
            messages.success(request, "Vehículo actualizado correctamente.")
            return redirect("courier:lista_vehiculos")
    else:
        datos = {
            "patente": vehiculo.patente, "tipo": vehiculo.tipo, "marca": vehiculo.marca,
            "modelo": vehiculo.modelo, "anio": vehiculo.anio, "capacidad_kg": vehiculo.capacidad_kg,
            "disponible": vehiculo.disponible, "estado": vehiculo.estado,
            "proveedor_id": vehiculo.proveedor_id,
        }

    return render(request, "courier/vehiculo_form.html", {
        "titulo": f"Editar vehículo · {vehiculo.patente}", "datos": datos, "errores": errores,
        "tipos": Vehiculo.TIPO_CHOICES, "estados": Vehiculo.ESTADO_CHOICES,
        "proveedores": Proveedor.objects.all(),
    })


@admin_requerido
def eliminar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)

    if request.method == "POST":
        vehiculo.delete()
        messages.success(request, "Vehículo eliminado correctamente.")
        return redirect("courier:lista_vehiculos")

    return render(request, "courier/confirmar_eliminar.html", {
        "objeto": vehiculo, "volver_url": "courier:lista_vehiculos",
    })


@login_required(login_url="courier:login")
def lista_conductores(request):
    """Listado de conductores."""
    contexto = {"conductores": Conductor.objects.select_related("vehiculo")}
    return render(request, "courier/lista_conductores.html", contexto)


def _leer_datos_conductor(request):
    datos = {
        "rut": request.POST.get("rut", "").strip(),
        "nombre": request.POST.get("nombre", "").strip(),
        "licencia": request.POST.get("licencia", "").strip(),
        "telefono": request.POST.get("telefono", "").strip(),
        "activo": request.POST.get("activo") == "on",
        "vehiculo_id": request.POST.get("vehiculo", ""),
    }

    errores = {}
    if not datos["nombre"]:
        errores["nombre"] = "El nombre es obligatorio."
    if not datos["licencia"]:
        errores["licencia"] = "La licencia es obligatoria."
    if not datos["telefono"]:
        errores["telefono"] = "El teléfono es obligatorio."

    return datos, errores


@admin_requerido
def crear_conductor(request):
    errores = {}
    datos = {}

    if request.method == "POST":
        datos, errores = _leer_datos_conductor(request)
        if not errores:
            vehiculo_id = datos.pop("vehiculo_id")
            Conductor.objects.create(vehiculo_id=vehiculo_id or None, **datos)
            messages.success(request, "Conductor creado correctamente.")
            return redirect("courier:lista_conductores")

    return render(request, "courier/conductor_form.html", {
        "titulo": "Nuevo conductor", "datos": datos, "errores": errores,
        "vehiculos": Vehiculo.objects.all(),
    })


@admin_requerido
def editar_conductor(request, conductor_id):
    conductor = get_object_or_404(Conductor, pk=conductor_id)
    errores = {}

    if request.method == "POST":
        datos, errores = _leer_datos_conductor(request)
        if not errores:
            vehiculo_id = datos.pop("vehiculo_id")
            for campo, valor in datos.items():
                setattr(conductor, campo, valor)
            conductor.vehiculo_id = vehiculo_id or None
            conductor.save()
            messages.success(request, "Conductor actualizado correctamente.")
            return redirect("courier:lista_conductores")
    else:
        datos = {
            "rut": conductor.rut, "nombre": conductor.nombre, "licencia": conductor.licencia,
            "telefono": conductor.telefono, "activo": conductor.activo,
            "vehiculo_id": conductor.vehiculo_id,
        }

    return render(request, "courier/conductor_form.html", {
        "titulo": f"Editar conductor · {conductor.nombre}", "datos": datos, "errores": errores,
        "vehiculos": Vehiculo.objects.all(),
    })


@admin_requerido
def eliminar_conductor(request, conductor_id):
    conductor = get_object_or_404(Conductor, pk=conductor_id)

    if request.method == "POST":
        conductor.delete()
        messages.success(request, "Conductor eliminado correctamente.")
        return redirect("courier:lista_conductores")

    return render(request, "courier/confirmar_eliminar.html", {
        "objeto": conductor, "volver_url": "courier:lista_conductores",
    })


@admin_requerido
def reportes(request):
    """Página de reportes: evidencia de las consultas resueltas con el ORM
    de Django (Parte 2 de la Evaluación 3), mostrando el código y el
    resultado real obtenido de la base de datos."""
    contexto = {"consultas": ejecutar_consultas()}
    return render(request, "courier/reportes.html", contexto)


@admin_requerido
def lista_usuarios(request):
    """CRUD de usuarios: listado, solo accesible para administradores (is_staff)."""
    contexto = {"usuarios": User.objects.all().order_by("username")}
    return render(request, "courier/usuarios/lista_usuarios.html", contexto)


@admin_requerido
def crear_usuario(request):
    errores = {}
    datos = {}

    if request.method == "POST":
        datos = {
            "username": request.POST.get("username", "").strip(),
            "first_name": request.POST.get("first_name", "").strip(),
            "last_name": request.POST.get("last_name", "").strip(),
            "email": request.POST.get("email", "").strip(),
            "is_staff": request.POST.get("is_staff") == "on",
            "is_active": request.POST.get("is_active") == "on",
        }
        password = request.POST.get("password", "")
        password_confirmacion = request.POST.get("password_confirmacion", "")

        if not datos["username"]:
            errores["username"] = "El usuario es obligatorio."
        elif User.objects.filter(username=datos["username"]).exists():
            errores["username"] = "Ya existe un usuario con ese nombre."
        if not password:
            errores["password"] = "La contraseña es obligatoria."
        elif len(password) < 8:
            errores["password"] = "La contraseña debe tener al menos 8 caracteres."
        elif password != password_confirmacion:
            errores["password_confirmacion"] = "Las contraseñas no coinciden."

        if not errores:
            usuario = User(**datos)
            usuario.set_password(password)
            usuario.save()
            messages.success(request, "Usuario creado correctamente.")
            return redirect("courier:lista_usuarios")

    return render(request, "courier/usuarios/form_usuario.html", {
        "titulo": "Nuevo usuario", "modo": "crear", "datos": datos, "errores": errores,
    })


@admin_requerido
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, pk=usuario_id)
    errores = {}

    if request.method == "POST":
        datos = {
            "username": request.POST.get("username", "").strip(),
            "first_name": request.POST.get("first_name", "").strip(),
            "last_name": request.POST.get("last_name", "").strip(),
            "email": request.POST.get("email", "").strip(),
            "is_staff": request.POST.get("is_staff") == "on",
            "is_active": request.POST.get("is_active") == "on",
        }

        if not datos["username"]:
            errores["username"] = "El usuario es obligatorio."
        elif User.objects.filter(username=datos["username"]).exclude(pk=usuario.pk).exists():
            errores["username"] = "Ya existe un usuario con ese nombre."

        if not errores:
            for campo, valor in datos.items():
                setattr(usuario, campo, valor)
            usuario.save()
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect("courier:lista_usuarios")
    else:
        datos = {
            "username": usuario.username, "first_name": usuario.first_name,
            "last_name": usuario.last_name, "email": usuario.email,
            "is_staff": usuario.is_staff, "is_active": usuario.is_active,
        }

    return render(request, "courier/usuarios/form_usuario.html", {
        "titulo": f"Editar usuario · {usuario.username}", "modo": "editar", "usuario": usuario,
        "datos": datos, "errores": errores,
    })


@admin_requerido
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, pk=usuario_id)

    if request.method == "POST":
        if usuario == request.user:
            messages.error(request, "No puedes eliminar tu propio usuario.")
        else:
            usuario.delete()
            messages.success(request, "Usuario eliminado correctamente.")
        return redirect("courier:lista_usuarios")

    return render(request, "courier/usuarios/confirmar_eliminar.html", {"usuario": usuario})
