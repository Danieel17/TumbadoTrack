from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from courier.data.seed_data import (
    BODEGAS,
    CLIENTES,
    ENVIOS,
    PRODUCTOS,
    PROVEEDORES,
    SEGUIMIENTO_EVENTOS,
)
from courier.models import Bodega, Cliente, Envio, Producto, Proveedor, SeguimientoEvento


class Command(BaseCommand):
    help = "Carga los datos de ejemplo de courier/data/seed_data.py en la base de datos."

    @transaction.atomic
    def handle(self, *args, **options):
        for item in PROVEEDORES:
            Proveedor.objects.update_or_create(id=item["id"], defaults={
                "nombre": item["nombre"],
                "pais": item["pais"],
                "email_contacto": item["email_contacto"],
                "telefono": item["telefono"],
                "tasa_puntualidad": item["tasa_puntualidad"],
                "activo": item["activo"],
            })

        for item in CLIENTES:
            Cliente.objects.update_or_create(id=item["id"], defaults={
                "nombre": item["nombre"],
                "ciudad": item["ciudad"],
                "tipo": item["tipo"],
                "email_contacto": item["email_contacto"],
                "telefono": item["telefono"],
            })

        for item in PRODUCTOS:
            Producto.objects.update_or_create(id=item["id"], defaults={
                "nombre": item["nombre"],
                "sku": item["sku"],
                "categoria": item["categoria"],
                "peso_kg": item["peso_kg"],
                "proveedor_id": item["proveedor_id"],
            })

        for item in BODEGAS:
            Bodega.objects.update_or_create(id=item["id"], defaults={
                "nombre": item["nombre"],
                "ubicacion": item["ubicacion"],
                "tipo": item["tipo"],
                "capacidad": item["capacidad"],
            })

        for item in ENVIOS:
            Envio.objects.update_or_create(id=item["id"], defaults={
                "codigo": item["codigo"],
                "producto_id": item["producto_id"],
                "proveedor_id": item["proveedor_id"],
                "cliente_id": item["cliente_id"],
                "destino": item["destino"],
                "peso_total_kg": item["peso_total_kg"],
                "estado": item["estado"],
                "fecha_envio": item["fecha_envio"],
                "fecha_estimada_entrega": item["fecha_estimada_entrega"],
                "fecha_real_entrega": item["fecha_real_entrega"],
                "ubicacion_actual": item["ubicacion_actual"],
            })

        for item in SEGUIMIENTO_EVENTOS:
            fecha_hora = timezone.make_aware(
                timezone.datetime.strptime(item["fecha_hora"], "%Y-%m-%d %H:%M")
            )
            SeguimientoEvento.objects.update_or_create(id=item["id"], defaults={
                "envio_id": item["envio_id"],
                "descripcion": item["descripcion"],
                "ubicacion": item["ubicacion"],
                "fecha_hora": fecha_hora,
            })

        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@tumbadotrack.local", "admin123")
            self.stdout.write(self.style.SUCCESS("Usuario demo creado: admin / admin123"))

        self.stdout.write(self.style.SUCCESS("Datos de ejemplo cargados correctamente."))
