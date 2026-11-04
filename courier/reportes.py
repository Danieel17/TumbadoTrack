"""
Las 20 consultas de referencia del caso "Transporte" (documento de la
Evaluación 3), aplicadas a nuestros modelos reales. Nuestro "Envío" cumple
el mismo rol que el "Viaje" del esquema de referencia: tiene vehículo,
conductor, origen, destino, fechas y estado.

El docente entrega 10 de estas 20 (o muy parecidas) como el informe oficial
a resolver. Mientras llega ese informe, aquí están las 20 ya resueltas,
listas para mostrar o ajustar.

Cada consulta es una función que devuelve (código como texto, resultado ya
ejecutado), para mostrarse en courier/templates/courier/reportes.html.
"""

from datetime import timedelta

from django.db.models import Avg, Count, F, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone

from .models import Conductor, Envio, Vehiculo


def _consulta_1():
    codigo = "Vehiculo.objects.all()"
    return codigo, list(Vehiculo.objects.all())


def _consulta_2():
    tipo_ejemplo = Vehiculo.objects.exclude(tipo="").values_list("tipo", flat=True).first()
    tipo_ejemplo = tipo_ejemplo or Vehiculo.TIPO_VAN
    codigo = f"Vehiculo.objects.filter(tipo='{tipo_ejemplo}')"
    return codigo, list(Vehiculo.objects.filter(tipo=tipo_ejemplo))


def _consulta_3():
    codigo = "Vehiculo.objects.filter(disponible=True)"
    return codigo, list(Vehiculo.objects.filter(disponible=True))


def _consulta_4():
    codigo = "Vehiculo.objects.exclude(anio__isnull=True).order_by('anio')[:10]"
    return codigo, list(Vehiculo.objects.exclude(anio__isnull=True).order_by("anio")[:10])


def _consulta_5():
    codigo = "Conductor.objects.count()"
    return codigo, Conductor.objects.count()


def _consulta_6():
    vehiculo = Vehiculo.objects.first()
    if vehiculo is None:
        return "Vehiculo.objects.first().envios.all()", []
    codigo = f"Vehiculo.objects.get(patente='{vehiculo.patente}').envios.all()"
    return codigo, list(vehiculo.envios.all())


def _consulta_7():
    conductor = Conductor.objects.first()
    if conductor is None:
        return "Conductor.objects.first().envios.all()", []
    codigo = f"Conductor.objects.get(licencia='{conductor.licencia}').envios.all()"
    return codigo, list(conductor.envios.all())


def _consulta_8():
    codigo = "Envio.objects.values('estado').annotate(total=Count('id')).order_by('-total')"
    filas = Envio.objects.values("estado").annotate(total=Count("id")).order_by("-total")
    nombres_estado = dict(Envio.ESTADO_CHOICES)
    return codigo, [f"{nombres_estado.get(f['estado'], f['estado'])}: {f['total']}" for f in filas]


def _consulta_9():
    hoy = timezone.now().date()
    desde = hoy - timedelta(days=30)
    codigo = f"Envio.objects.filter(fecha_envio__range=['{desde}', '{hoy}'])"
    return codigo, list(Envio.objects.filter(fecha_envio__range=[desde, hoy]))


def _consulta_10():
    codigo = "Vehiculo.objects.filter(envios__isnull=True)"
    return codigo, list(Vehiculo.objects.filter(envios__isnull=True))


def _consulta_11():
    codigo = "Conductor.objects.annotate(total_viajes=Count('envios')).order_by('-total_viajes')[:5]"
    filas = Conductor.objects.annotate(total_viajes=Count("envios")).order_by("-total_viajes")[:5]
    return codigo, [f"{c.nombre}: {c.total_viajes} viajes" for c in filas]


def _consulta_12():
    codigo = "Vehiculo.objects.annotate(total_viajes=Count('envios')).order_by('-total_viajes')[:5]"
    filas = Vehiculo.objects.annotate(total_viajes=Count("envios")).order_by("-total_viajes")[:5]
    return codigo, [f"{v.patente}: {v.total_viajes} viajes" for v in filas]


def _consulta_13():
    hace_un_mes = timezone.now().date() - timedelta(days=30)
    codigo = (
        "Conductor.objects.annotate(\n"
        "    viajes_ultimo_mes=Count('envios', filter=Q(envios__fecha_envio__gte=hace_un_mes))\n"
        ")"
    )
    filas = Conductor.objects.annotate(
        viajes_ultimo_mes=Count("envios", filter=Q(envios__fecha_envio__gte=hace_un_mes))
    )
    return codigo, [f"{c.nombre}: {c.viajes_ultimo_mes} viajes" for c in filas]


def _consulta_14():
    codigo = "Envio.objects.values('vehiculo__tipo').annotate(total=Count('id')).order_by('-total')"
    filas = Envio.objects.exclude(vehiculo__isnull=True).values("vehiculo__tipo").annotate(
        total=Count("id")
    ).order_by("-total")
    nombres_tipo = dict(Vehiculo.TIPO_CHOICES)
    return codigo, [f"{nombres_tipo.get(f['vehiculo__tipo'], f['vehiculo__tipo'])}: {f['total']}" for f in filas]


def _consulta_15():
    codigo = "Envio.objects.values('destino').annotate(total=Count('id')).order_by('-total')"
    filas = Envio.objects.values("destino").annotate(total=Count("id")).order_by("-total")[:10]
    return codigo, [f"{f['destino']}: {f['total']}" for f in filas]


def _consulta_16():
    hace_un_mes = timezone.now().date() - timedelta(days=30)
    codigo = (
        "Conductor.objects.exclude(\n"
        "    envios__fecha_envio__gte=hace_un_mes\n"
        ").distinct()"
    )
    resultado = Conductor.objects.exclude(envios__fecha_envio__gte=hace_un_mes).distinct()
    return codigo, list(resultado)


def _consulta_17():
    codigo = (
        "Envio.objects.filter(estado=Envio.ESTADO_ENTREGADO, fecha_real_entrega__isnull=False)\n"
        "    .annotate(duracion=F('fecha_real_entrega') - F('fecha_envio'))\n"
        "    .aggregate(Avg('duracion'))"
    )
    resultado = Envio.objects.filter(
        estado=Envio.ESTADO_ENTREGADO, fecha_real_entrega__isnull=False
    ).annotate(duracion=F("fecha_real_entrega") - F("fecha_envio")).aggregate(promedio=Avg("duracion"))
    promedio = resultado["promedio"]
    if promedio is None:
        return codigo, "Sin envíos entregados todavía."
    return codigo, f"{promedio.days} días en promedio"


def _consulta_18():
    anio_actual = timezone.now().year
    codigo = (
        "Conductor.objects.filter(envios__estado=Envio.ESTADO_ENTREGADO, envios__fecha_envio__year=anio_actual)\n"
        "    .annotate(total=Count('envios')).order_by('-total').first()"
    )
    conductor = Conductor.objects.filter(
        envios__estado=Envio.ESTADO_ENTREGADO, envios__fecha_envio__year=anio_actual
    ).annotate(total=Count("envios")).order_by("-total").first()
    if conductor is None:
        return codigo, "Sin envíos entregados este año."
    return codigo, f"{conductor.nombre} ({conductor.total} viajes finalizados)"


def _consulta_19():
    codigo = "Envio.objects.values('estado').annotate(total=Count('id'))  # con porcentaje calculado en Python"
    total = Envio.objects.count()
    if total == 0:
        return codigo, "Sin envíos registrados."
    finalizados = Envio.objects.filter(estado=Envio.ESTADO_ENTREGADO).count()
    cancelados = Envio.objects.filter(estado=Envio.ESTADO_CANCELADO).count()
    pendientes = total - finalizados - cancelados
    resultado = [
        f"Finalizado: {finalizados / total * 100:.1f}%",
        f"Cancelado: {cancelados / total * 100:.1f}%",
        f"Pendiente: {pendientes / total * 100:.1f}%",
    ]
    return codigo, resultado


MESES_ES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]


def _consulta_20():
    anio_actual = timezone.now().year
    codigo = (
        "Envio.objects.filter(fecha_envio__year=anio_actual)\n"
        "    .annotate(mes=TruncMonth('fecha_envio')).values('mes')\n"
        "    .annotate(total=Count('id')).order_by('mes')"
    )
    filas = Envio.objects.filter(fecha_envio__year=anio_actual).annotate(
        mes=TruncMonth("fecha_envio")
    ).values("mes").annotate(total=Count("id")).order_by("mes")
    resultado = [
        f"{MESES_ES[f['mes'].month - 1].capitalize()} {f['mes'].year}: {f['total']} viajes" for f in filas
    ]
    return codigo, resultado


CONSULTAS = [
    {"n": 1, "nivel": "Básico", "pregunta": "¿Cuáles son todos los vehículos registrados en el sistema?", "fn": _consulta_1},
    {"n": 2, "nivel": "Básico", "pregunta": "¿Qué vehículos pertenecen a un tipo seleccionado?", "fn": _consulta_2},
    {"n": 3, "nivel": "Básico", "pregunta": "¿Cuáles son los vehículos que se encuentran disponibles?", "fn": _consulta_3},
    {"n": 4, "nivel": "Básico", "pregunta": "¿Cuáles son los 10 vehículos más antiguos de la empresa?", "fn": _consulta_4},
    {"n": 5, "nivel": "Básico", "pregunta": "¿Cuántos conductores están registrados en el sistema?", "fn": _consulta_5},
    {"n": 6, "nivel": "Intermedio", "pregunta": "¿Cuáles son los viajes realizados por un vehículo específico?", "fn": _consulta_6},
    {"n": 7, "nivel": "Intermedio", "pregunta": "¿Qué viajes tiene asignados un conductor seleccionado?", "fn": _consulta_7},
    {"n": 8, "nivel": "Intermedio", "pregunta": "¿Cuántos viajes se encuentran programados, en curso, finalizados o cancelados?", "fn": _consulta_8},
    {"n": 9, "nivel": "Intermedio", "pregunta": "¿Cuáles son los viajes programados durante un rango de fechas?", "fn": _consulta_9},
    {"n": 10, "nivel": "Intermedio", "pregunta": "¿Qué vehículos no tienen viajes registrados?", "fn": _consulta_10},
    {"n": 11, "nivel": "Intermedio", "pregunta": "¿Cuáles son los cinco conductores que han realizado más viajes?", "fn": _consulta_11},
    {"n": 12, "nivel": "Intermedio", "pregunta": "¿Cuáles son los cinco vehículos que han participado en más viajes?", "fn": _consulta_12},
    {"n": 13, "nivel": "Avanzado", "pregunta": "¿Cuántos viajes ha realizado cada conductor durante el último mes?", "fn": _consulta_13},
    {"n": 14, "nivel": "Avanzado", "pregunta": "¿Qué tipos de vehículos se utilizan con mayor frecuencia en los viajes?", "fn": _consulta_14},
    {"n": 15, "nivel": "Avanzado", "pregunta": "¿Cuántos viajes se han realizado hacia cada destino?", "fn": _consulta_15},
    {"n": 16, "nivel": "Avanzado", "pregunta": "¿Qué conductores no han realizado viajes durante un período seleccionado?", "fn": _consulta_16},
    {"n": 17, "nivel": "Avanzado", "pregunta": "¿Cuál es la duración promedio de los viajes finalizados?", "fn": _consulta_17},
    {"n": 18, "nivel": "Análisis", "pregunta": "¿Qué conductor ha acumulado la mayor cantidad de viajes finalizados durante el año?", "fn": _consulta_18},
    {"n": 19, "nivel": "Análisis", "pregunta": "¿Qué porcentaje de los viajes registrados se encuentra finalizado, cancelado o pendiente?", "fn": _consulta_19},
    {"n": 20, "nivel": "Análisis", "pregunta": "¿Cómo se distribuye la cantidad de viajes realizados por mes durante el año seleccionado?", "fn": _consulta_20},
]


def ejecutar_consultas():
    """Ejecuta las 20 consultas y devuelve una lista lista para el template,
    con el código usado y el resultado real obtenido de la base de datos.

    Cada resultado se normaliza a una lista de strings (es_lista=True) o a
    un único string (es_lista=False), para que el template no tenga que
    adivinar el tipo de dato que devolvió cada consulta."""
    salida = []
    for item in CONSULTAS:
        codigo, resultado = item["fn"]()

        if isinstance(resultado, (list, tuple)) or hasattr(resultado, "all"):
            lista = [str(obj) for obj in resultado]
            salida.append({
                "n": item["n"], "nivel": item["nivel"], "pregunta": item["pregunta"],
                "codigo": codigo, "es_lista": True, "resultado": lista,
            })
        else:
            valor = "Sin resultado." if resultado is None else str(resultado)
            salida.append({
                "n": item["n"], "nivel": item["nivel"], "pregunta": item["pregunta"],
                "codigo": codigo, "es_lista": False, "resultado": valor,
            })
    return salida
