from django.db import models


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150)
    pais = models.CharField(max_length=100)
    email_contacto = models.EmailField()
    telefono = models.CharField(max_length=30)
    tasa_puntualidad = models.DecimalField(max_digits=4, decimal_places=1)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    TIPO_VENUE = "venue"
    TIPO_ESTUDIO = "estudio"
    TIPO_CHOICES = [
        (TIPO_VENUE, "Venue"),
        (TIPO_ESTUDIO, "Estudio"),
    ]

    nombre = models.CharField(max_length=150)
    ciudad = models.CharField(max_length=150)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    email_contacto = models.EmailField()
    telefono = models.CharField(max_length=30)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    CATEGORIA_INSTRUMENTO = "instrumento"
    CATEGORIA_SONIDO = "sonido"
    CATEGORIA_ILUMINACION = "iluminacion"
    CATEGORIA_CHOICES = [
        (CATEGORIA_INSTRUMENTO, "Instrumento"),
        (CATEGORIA_SONIDO, "Sonido"),
        (CATEGORIA_ILUMINACION, "Iluminación"),
    ]

    nombre = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    peso_kg = models.DecimalField(max_digits=7, decimal_places=1)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name="productos")

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Bodega(models.Model):
    TIPO_PRINCIPAL = "principal"
    TIPO_SUCURSAL = "sucursal"
    TIPO_CHOICES = [
        (TIPO_PRINCIPAL, "Principal"),
        (TIPO_SUCURSAL, "Sucursal"),
    ]

    nombre = models.CharField(max_length=150)
    ubicacion = models.CharField(max_length=150)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    capacidad = models.PositiveIntegerField()

    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Bodegas"

    def __str__(self):
        return self.nombre


class Envio(models.Model):
    ESTADO_PREPARANDO = "preparando"
    ESTADO_EN_TRANSITO = "en_transito"
    ESTADO_EN_ADUANA = "en_aduana"
    ESTADO_ENTREGADO = "entregado"
    ESTADO_CHOICES = [
        (ESTADO_PREPARANDO, "Preparando"),
        (ESTADO_EN_TRANSITO, "En tránsito"),
        (ESTADO_EN_ADUANA, "En aduana"),
        (ESTADO_ENTREGADO, "Entregado"),
    ]

    codigo = models.CharField(max_length=30, unique=True)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name="envios")
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name="envios")
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="envios")
    destino = models.CharField(max_length=200)
    peso_total_kg = models.DecimalField(max_digits=7, decimal_places=1)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_PREPARANDO)
    fecha_envio = models.DateField()
    fecha_estimada_entrega = models.DateField()
    fecha_real_entrega = models.DateField(null=True, blank=True)
    ubicacion_actual = models.CharField(max_length=200)

    class Meta:
        ordering = ["-fecha_envio"]

    def __str__(self):
        return self.codigo


class SeguimientoEvento(models.Model):
    envio = models.ForeignKey(Envio, on_delete=models.CASCADE, related_name="eventos")
    descripcion = models.CharField(max_length=255)
    ubicacion = models.CharField(max_length=200)
    fecha_hora = models.DateTimeField()

    class Meta:
        ordering = ["fecha_hora"]
        verbose_name = "Evento de seguimiento"
        verbose_name_plural = "Eventos de seguimiento"

    def __str__(self):
        return f"{self.envio.codigo} · {self.descripcion}"
