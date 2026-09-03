from functools import wraps

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import ProtectedError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ClienteForm, EnvioForm, ProveedorForm, UsuarioCreationForm, UsuarioEditForm
from .models import Cliente, Envio, Proveedor


def login_requerido(vista):
    """Redirige a /login/ si el usuario no ha iniciado sesión."""
    @wraps(vista)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("courier:login")
        return vista(request, *args, **kwargs)
    return wrapper


def admin_requerido(vista):
    """Además de exigir sesión iniciada, exige rol de administrador (is_staff)."""
    @wraps(vista)
    @login_requerido
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return vista(request, *args, **kwargs)
    return wrapper


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
    logout(request)
    return redirect("courier:landing")


@login_requerido
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


@login_requerido
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


@login_requerido
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


@admin_requerido
def crear_envio(request):
    if request.method == "POST":
        form = EnvioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Envío creado correctamente.")
            return redirect("courier:lista_envios")
    else:
        form = EnvioForm()

    return render(request, "courier/form_generico.html", {
        "form": form, "titulo": "Nuevo envío", "volver_url": "courier:lista_envios",
    })


@admin_requerido
def editar_envio(request, envio_id):
    envio = get_object_or_404(Envio, pk=envio_id)

    if request.method == "POST":
        form = EnvioForm(request.POST, instance=envio)
        if form.is_valid():
            form.save()
            messages.success(request, "Envío actualizado correctamente.")
            return redirect("courier:detalle_envio", envio_id=envio.id)
    else:
        form = EnvioForm(instance=envio)

    return render(request, "courier/form_generico.html", {
        "form": form, "titulo": f"Editar envío · {envio.codigo}", "volver_url": "courier:detalle_envio",
        "volver_args": [envio.id],
    })


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


@login_requerido
def lista_proveedores(request):
    """Listado de proveedores de equipos musicales."""
    contexto = {"proveedores": Proveedor.objects.all()}
    return render(request, "courier/lista_proveedores.html", contexto)


@admin_requerido
def crear_proveedor(request):
    if request.method == "POST":
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor creado correctamente.")
            return redirect("courier:lista_proveedores")
    else:
        form = ProveedorForm()

    return render(request, "courier/form_generico.html", {
        "form": form, "titulo": "Nuevo proveedor", "volver_url": "courier:lista_proveedores",
    })


@admin_requerido
def editar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, pk=proveedor_id)

    if request.method == "POST":
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor actualizado correctamente.")
            return redirect("courier:lista_proveedores")
    else:
        form = ProveedorForm(instance=proveedor)

    return render(request, "courier/form_generico.html", {
        "form": form, "titulo": f"Editar proveedor · {proveedor.nombre}", "volver_url": "courier:lista_proveedores",
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


@login_requerido
def lista_clientes(request):
    """Listado de clientes (recintos/venues del tour)."""
    contexto = {"clientes": Cliente.objects.all()}
    return render(request, "courier/lista_clientes.html", contexto)


@admin_requerido
def crear_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente creado correctamente.")
            return redirect("courier:lista_clientes")
    else:
        form = ClienteForm()

    return render(request, "courier/form_generico.html", {
        "form": form, "titulo": "Nuevo cliente", "volver_url": "courier:lista_clientes",
    })


@admin_requerido
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)

    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente actualizado correctamente.")
            return redirect("courier:lista_clientes")
    else:
        form = ClienteForm(instance=cliente)

    return render(request, "courier/form_generico.html", {
        "form": form, "titulo": f"Editar cliente · {cliente.nombre}", "volver_url": "courier:lista_clientes",
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


@admin_requerido
def lista_usuarios(request):
    """CRUD de usuarios: listado, solo accesible para administradores (is_staff)."""
    contexto = {"usuarios": User.objects.all().order_by("username")}
    return render(request, "courier/usuarios/lista_usuarios.html", contexto)


@admin_requerido
def crear_usuario(request):
    if request.method == "POST":
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado correctamente.")
            return redirect("courier:lista_usuarios")
    else:
        form = UsuarioCreationForm()

    return render(request, "courier/usuarios/form_usuario.html", {"form": form, "modo": "crear"})


@admin_requerido
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, pk=usuario_id)

    if request.method == "POST":
        form = UsuarioEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect("courier:lista_usuarios")
    else:
        form = UsuarioEditForm(instance=usuario)

    return render(request, "courier/usuarios/form_usuario.html", {"form": form, "modo": "editar", "usuario": usuario})


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
