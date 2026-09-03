from django.http import Http404
from django.shortcuts import render

from .data import repository


def dashboard(request):
    """Vista principal: estadísticas generales del sistema de courier."""
    contexto = {
        "estadisticas": repository.get_estadisticas_dashboard(),
        "envios_recientes": repository.get_envios()[-5:][::-1],
    }
    return render(request, "courier/dashboard.html", contexto)


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


def lista_proveedores(request):
    """Listado de proveedores de equipos musicales."""
    contexto = {"proveedores": repository.get_proveedores()}
    return render(request, "courier/lista_proveedores.html", contexto)


def lista_clientes(request):
    """Listado de clientes (recintos/venues del tour)."""
    contexto = {"clientes": repository.get_clientes()}
    return render(request, "courier/lista_clientes.html", contexto)
