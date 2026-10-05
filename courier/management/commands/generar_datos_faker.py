from django.core.management.base import BaseCommand
from django.utils import timezone
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
from faker import Faker
import random


class Command(BaseCommand):
    help = "Genera proveedores, clientes, vehículos, conductores y envíos de prueba con Faker"

    def handle(self, *args, **kwargs):

        fake = Faker("es_CL")

        tipos_vehiculo = [
            Vehiculo.TIPO_CAMION,
            Vehiculo.TIPO_VAN,
            Vehiculo.TIPO_TRAILER
        ]

        tipos_cliente = [
            Cliente.TIPO_VENUE,
            Cliente.TIPO_ESTUDIO
        ]

        tipos_incidencia = [
            Incidencia.TIPO_RETRASO,
            Incidencia.TIPO_DESVIO,
            Incidencia.TIPO_FALLA_MECANICA,
            Incidencia.TIPO_OTRO
        ]

        estados_envio = [
            Envio.ESTADO_PREPARANDO,
            Envio.ESTADO_EN_TRANSITO,
            Envio.ESTADO_EN_ADUANA,
            Envio.ESTADO_ENTREGADO
        ]

        proveedores = []

        for i in range(5):

            proveedor = Proveedor.objects.create(
                nombre=fake.company(),

                pais=fake.country(),

                email_contacto=fake.unique.company_email(),

                telefono=fake.phone_number(),

                tasa_puntualidad=round(
                    random.uniform(80, 99), 1
                ),

                activo=fake.boolean(
                    chance_of_getting_true=85
                )
            )

            proveedores.append(proveedor)

        clientes = []

        for i in range(6):

            cliente = Cliente.objects.create(
                nombre=f"{fake.company()} Arena",

                ciudad=fake.city(),

                tipo=random.choice(tipos_cliente),

                email_contacto=fake.unique.email(),

                telefono=fake.phone_number()
            )

            clientes.append(cliente)

        vehiculos = []

        for i in range(6):

            vehiculo = Vehiculo.objects.create(
                patente=fake.unique.bothify(
                    text="??-####"
                ).upper(),

                tipo=random.choice(tipos_vehiculo),

                capacidad_kg=round(
                    random.uniform(500, 8000), 1
                ),

                proveedor=random.choice(proveedores)
            )

            vehiculos.append(vehiculo)

        conductores = []

        for i in range(6):

            conductor = Conductor.objects.create(
                nombre=fake.name(),

                licencia=fake.unique.bothify(
                    text="LIC-########"
                ),

                telefono=fake.phone_number(),

                vehiculo=random.choice(vehiculos)
            )

            conductores.append(conductor)

        productos = list(Producto.objects.all())

        if not productos:

            self.stdout.write(
                self.style.WARNING(
                    "No hay productos en la base de datos: corre antes 'python manage.py seed_datos'."
                )
            )
            return

        for i in range(15):

            fecha_envio = fake.date_between(
                start_date="-60d", end_date="-5d"
            )

            fecha_estimada = fake.date_between(
                start_date=fecha_envio, end_date="+20d"
            )

            estado = random.choice(estados_envio)

            envio = Envio.objects.create(
                codigo=f"MPC-FK-{fake.unique.random_number(digits=5)}",

                producto=random.choice(productos),

                proveedor=random.choice(proveedores),

                cliente=random.choice(clientes),

                vehiculo=random.choice(vehiculos),

                conductor=random.choice(conductores),

                destino=f"{fake.city()}, {fake.country()}",

                peso_total_kg=round(
                    random.uniform(20, 900), 1
                ),

                estado=estado,

                fecha_envio=fecha_envio,

                fecha_estimada_entrega=fecha_estimada,

                fecha_real_entrega=fecha_estimada if estado == Envio.ESTADO_ENTREGADO else None,

                ubicacion_actual=fake.city()
            )

            SeguimientoEvento.objects.create(
                envio=envio,

                descripcion="Envío registrado en el sistema",

                ubicacion=fake.city(),

                fecha_hora=timezone.make_aware(
                    fake.date_time_between(start_date=fecha_envio, end_date="now")
                )
            )

            if random.random() < 0.3:

                Incidencia.objects.create(
                    envio=envio,

                    tipo=random.choice(tipos_incidencia),

                    descripcion=fake.sentence(nb_words=8),

                    fecha_hora=timezone.make_aware(
                        fake.date_time_between(start_date=fecha_envio, end_date="now")
                    )
                )

            if estado == Envio.ESTADO_ENTREGADO:

                ComprobanteEntrega.objects.create(
                    envio=envio,

                    nombre_receptor=fake.name(),

                    codigo_escaneado=fake.bothify(
                        text="QR-########"
                    ),

                    fecha_hora=timezone.make_aware(
                        fake.date_time_between(start_date=fecha_estimada, end_date="now")
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Proveedores, clientes, vehículos, conductores y envíos creados correctamente."
            )
        )
