"""
Consultas de práctica para la Parte 2 de la Evaluación 3 ("Desarrollo de
consultas utilizando Django ORM"). Siguen el estilo de las preguntas de
ejemplo del caso "Transporte" del enunciado (listar, buscar por tipo,
contar, ordenar, relaciones, actualizar, agregaciones).

Cuando el docente entregue el informe oficial con las 10 consultas reales,
se reemplazan aquí mismo: cada consulta es una función que devuelve
(código como texto, resultado ya ejecutado), para mostrarlos en
courier/templates/courier/reportes.html.
"""

from django.db.models import Count

from .models import Conductor, Envio, Vehiculo


def _consulta_1():
    codigo = "Vehiculo.objects.all()"
    resultado = list(Vehiculo.objects.all())
    return codigo, resultado


def _consulta_2():
    codigo = 'Vehiculo.objects.filter(tipo=Vehiculo.TIPO_CAMION)'
    resultado = list(Vehiculo.objects.filter(tipo=Vehiculo.TIPO_CAMION))
    return codigo, resultado


def _consulta_3():
    codigo = (
        "Vehiculo.objects.exclude(\n"
        "    envios__estado__in=[Envio.ESTADO_EN_TRANSITO, Envio.ESTADO_EN_ADUANA]\n"
        ").distinct()"
    )
    resultado = list(
        Vehiculo.objects.exclude(
            envios__estado__in=[Envio.ESTADO_EN_TRANSITO, Envio.ESTADO_EN_ADUANA]
        ).distinct()
    )
    return codigo, resultado


def _consulta_4():
    codigo = "Vehiculo.objects.order_by('-capacidad_kg')"
    resultado = list(Vehiculo.objects.order_by("-capacidad_kg")[:10])
    return codigo, resultado


def _consulta_5():
    codigo = "Conductor.objects.count()"
    resultado = Conductor.objects.count()
    return codigo, resultado


def _consulta_6():
    vehiculo = Vehiculo.objects.first()
    if vehiculo is None:
        return "Vehiculo.objects.first().envios.all()", []
    codigo = f"Vehiculo.objects.get(patente='{vehiculo.patente}').envios.all()"
    resultado = list(vehiculo.envios.all())
    return codigo, resultado


def _consulta_7():
    conductor = Conductor.objects.first()
    if conductor is None:
        return "Conductor.objects.first().envios.all()", []
    codigo = f"Conductor.objects.get(licencia='{conductor.licencia}').envios.all()"
    resultado = list(conductor.envios.all())
    return codigo, resultado


def _consulta_8():
    codigo = "Envio.objects.values('estado').annotate(total=Count('id')).order_by('-total')"
    filas = Envio.objects.values("estado").annotate(total=Count("id")).order_by("-total")
    nombres_estado = dict(Envio.ESTADO_CHOICES)
    resultado = [f"{nombres_estado.get(f['estado'], f['estado'])}: {f['total']}" for f in filas]
    return codigo, resultado


def _consulta_9():
    codigo = "Vehiculo.objects.filter(envios__isnull=True)"
    resultado = list(Vehiculo.objects.filter(envios__isnull=True))
    return codigo, resultado


def _consulta_10():
    codigo = "Envio.objects.order_by('-fecha_envio').first()"
    resultado = Envio.objects.order_by("-fecha_envio").first()
    return codigo, resultado


CONSULTAS = [
    {"n": 1, "nivel": "Básico", "pregunta": "¿Cuáles son todos los vehículos registrados en el sistema?", "fn": _consulta_1},
    {"n": 2, "nivel": "Básico", "pregunta": "¿Qué vehículos son de tipo Camión?", "fn": _consulta_2},
    {"n": 3, "nivel": "Básico", "pregunta": "¿Qué vehículos están disponibles (sin envíos en tránsito o en aduana)?", "fn": _consulta_3},
    {"n": 4, "nivel": "Básico", "pregunta": "¿Cuáles son los 10 vehículos con mayor capacidad de carga?", "fn": _consulta_4},
    {"n": 5, "nivel": "Intermedio", "pregunta": "¿Cuántos conductores están registrados en el sistema?", "fn": _consulta_5},
    {"n": 6, "nivel": "Intermedio", "pregunta": "¿Cuáles son los envíos realizados por un vehículo específico?", "fn": _consulta_6},
    {"n": 7, "nivel": "Intermedio", "pregunta": "¿Qué envíos tiene asignados un conductor específico?", "fn": _consulta_7},
    {"n": 8, "nivel": "Intermedio", "pregunta": "¿Cuántos envíos hay por cada estado (preparando, en tránsito, en aduana, entregado)?", "fn": _consulta_8},
    {"n": 9, "nivel": "Avanzado", "pregunta": "¿Qué vehículos no tienen envíos registrados?", "fn": _consulta_9},
    {"n": 10, "nivel": "Avanzado", "pregunta": "¿Cuál fue el envío más reciente registrado?", "fn": _consulta_10},
]


def ejecutar_consultas():
    """Ejecuta las 10 consultas y devuelve una lista lista para el template,
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
