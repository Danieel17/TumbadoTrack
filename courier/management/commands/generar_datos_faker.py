import random

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from faker import Faker

from courier.models import (
    Cliente,
    ComprobanteEntrega,
    Conductor,
    Envio,
    Incidencia,
    Producto,
    Proveedor,
    SeguimientoEvento,
    Vehiculo,
)


class Command(BaseCommand):
    """Genera datos ficticios con Faker para probar la aplicación con un volumen
    mayor de registros, además de los datos curados de courier/data/seed_data.py.

    Uso: python manage.py generar_datos_faker [--cantidad 15]
    """

    help = "Genera datos de prueba con Faker (proveedores, clientes, vehículos, conductores y envíos)."

    def add_arguments(self, parser):
        parser.add_argument("--cantidad", type=int, default=15, help="Cantidad de envíos ficticios a crear.")

    @transaction.atomic
    def handle(self, *args, **options):
        fake = Faker("es_CL")
        cantidad = options["cantidad"]

        proveedores = self._crear_proveedores(fake, cantidad=5)
        clientes = self._crear_clientes(fake, cantidad=6)
        vehiculos = self._crear_vehiculos(fake, proveedores, cantidad=6)
        conductores = self._crear_conductores(fake, vehiculos, cantidad=6)
        envios = self._crear_envios(fake, proveedores, clientes, vehiculos, conductores, cantidad=cantidad)

        self.stdout.write(self.style.SUCCESS(
            f"Listo: {len(proveedores)} proveedores, {len(clientes)} clientes, "
            f"{len(vehiculos)} vehículos, {len(conductores)} conductores y "
            f"{len(envios)} envíos (con sus eventos/incidencias/comprobantes) generados con Faker."
        ))

    def _crear_proveedores(self, fake, cantidad):
        proveedores = []
        for _ in range(cantidad):
            proveedor, _ = Proveedor.objects.get_or_create(
                email_contacto=fake.unique.company_email(),
                defaults={
                    "nombre": fake.company(),
                    "pais": fake.country(),
                    "telefono": fake.phone_number(),
                    "tasa_puntualidad": round(random.uniform(80, 99), 1),
                    "activo": fake.boolean(chance_of_getting_true=85),
                },
            )
            proveedores.append(proveedor)
        return proveedores

    def _crear_clientes(self, fake, cantidad):
        clientes = []
        for _ in range(cantidad):
            cliente, _ = Cliente.objects.get_or_create(
                email_contacto=fake.unique.email(),
                defaults={
                    "nombre": f"{fake.company()} {random.choice(['Arena', 'Estadio', 'Teatro', 'Club'])}",
                    "ciudad": fake.city(),
                    "tipo": random.choice([Cliente.TIPO_VENUE, Cliente.TIPO_ESTUDIO]),
                    "telefono": fake.phone_number(),
                },
            )
            clientes.append(cliente)
        return clientes

    def _crear_vehiculos(self, fake, proveedores, cantidad):
        vehiculos = []
        for _ in range(cantidad):
            patente = fake.unique.bothify(text="??-####").upper()
            vehiculo, _ = Vehiculo.objects.get_or_create(
                patente=patente,
                defaults={
                    "tipo": random.choice([Vehiculo.TIPO_CAMION, Vehiculo.TIPO_VAN, Vehiculo.TIPO_TRAILER]),
                    "capacidad_kg": round(random.uniform(500, 8000), 1),
                    "proveedor": random.choice(proveedores),
                },
            )
            vehiculos.append(vehiculo)
        return vehiculos

    def _crear_conductores(self, fake, vehiculos, cantidad):
        conductores = []
        for _ in range(cantidad):
            licencia = fake.unique.bothify(text="LIC-########")
            conductor, _ = Conductor.objects.get_or_create(
                licencia=licencia,
                defaults={
                    "nombre": fake.name(),
                    "telefono": fake.phone_number(),
                    "vehiculo": random.choice(vehiculos) if vehiculos else None,
                },
            )
            conductores.append(conductor)
        return conductores

    def _crear_envios(self, fake, proveedores, clientes, vehiculos, conductores, cantidad):
        productos = list(Producto.objects.all())
        if not productos:
            self.stdout.write(self.style.WARNING(
                "No hay Productos en la base de datos: corre antes 'python manage.py seed_datos'."
            ))
            return []

        envios = []
        for _ in range(cantidad):
            codigo = f"MPC-FK-{fake.unique.random_number(digits=5)}"
            estado = random.choice([c[0] for c in Envio.ESTADO_CHOICES])
            fecha_envio = fake.date_between(start_date="-60d", end_date="-5d")
            fecha_estimada = fake.date_between(start_date=fecha_envio, end_date="+20d")
            fecha_real = fecha_estimada if estado == Envio.ESTADO_ENTREGADO else None

            envio = Envio.objects.create(
                codigo=codigo,
                producto=random.choice(productos),
                proveedor=random.choice(proveedores),
                cliente=random.choice(clientes),
                vehiculo=random.choice(vehiculos) if vehiculos else None,
                conductor=random.choice(conductores) if conductores else None,
                destino=f"{fake.city()}, {fake.country()}",
                peso_total_kg=round(random.uniform(20, 900), 1),
                estado=estado,
                fecha_envio=fecha_envio,
                fecha_estimada_entrega=fecha_estimada,
                fecha_real_entrega=fecha_real,
                ubicacion_actual=fake.city(),
            )
            envios.append(envio)

            SeguimientoEvento.objects.create(
                envio=envio,
                descripcion="Envío registrado en el sistema",
                ubicacion=fake.city(),
                fecha_hora=timezone.make_aware(
                    fake.date_time_between(start_date=fecha_envio, end_date="now")
                ),
            )

            if random.random() < 0.3:
                Incidencia.objects.create(
                    envio=envio,
                    tipo=random.choice([c[0] for c in Incidencia.TIPO_CHOICES]),
                    descripcion=fake.sentence(nb_words=8),
                    fecha_hora=timezone.make_aware(
                        fake.date_time_between(start_date=fecha_envio, end_date="now")
                    ),
                )

            if estado == Envio.ESTADO_ENTREGADO:
                ComprobanteEntrega.objects.get_or_create(
                    envio=envio,
                    defaults={
                        "nombre_receptor": fake.name(),
                        "firma_url": "",
                        "foto_url": "",
                        "codigo_escaneado": fake.bothify(text="QR-########"),
                        "fecha_hora": timezone.make_aware(
                            fake.date_time_between(start_date=fecha_estimada, end_date="now")
                        ),
                    },
                )

        return envios
