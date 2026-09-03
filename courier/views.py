from functools import wraps

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .data import repository
from .forms import UsuarioCreationForm, UsuarioEditForm


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
        "estadisticas": repository.get_estadisticas_dashboard(),
        "envios_recientes": repository.get_envios()[-5:][::-1],
    }
    return render(request, "courier/dashboard.html", contexto)


@login_requerido
def lista_envios(request):
    """Listado de todos los envíos, con sus relaciones ya resueltas."""
    estado_filtro = request.GET.get("estado")

    if estado_filtro:
        envios = repository.get_envios_by_estado(estado_filtro)
    else:
        envios = repository.get_envios()

    envios_completos = [repository.enriquecer_envio(e) for e in envios]

    contexto = {
        "envios": envios_completos,
        "estado_filtro": estado_filtro,
    }
    return render(request, "courier/lista_envios.html", contexto)


@login_requerido
def detalle_envio(request, envio_id):
    """Detalle y tracking de un envío específico, con su historial de eventos."""
    envio = repository.enriquecer_envio(repository.get_envio(envio_id))
    if envio is None:
        raise Http404("El envío solicitado no existe.")

    contexto = {
        "envio": envio,
        "eventos": repository.get_eventos_by_envio(envio_id),
    }
    return render(request, "courier/detalle_envio.html", contexto)


@login_requerido
def lista_proveedores(request):
    """Listado de proveedores de equipos musicales."""
    contexto = {"proveedores": repository.get_proveedores()}
    return render(request, "courier/lista_proveedores.html", contexto)


@login_requerido
def lista_clientes(request):
    """Listado de clientes (recintos/venues del tour)."""
    contexto = {"clientes": repository.get_clientes()}
    return render(request, "courier/lista_clientes.html", contexto)


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
