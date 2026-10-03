from django.db import models


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150)
    pais = models.CharField(max_length=100, verbose_name="País")
    email_contacto = models.EmailField(verbose_name="Correo de contacto")
    telefono = models.CharField(max_length=30, verbose_name="Teléfono")
    tasa_puntualidad = models.DecimalField(max_digits=4, decimal_places=1, verbose_name="Tasa de puntualidad (%)")
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
    email_contacto = models.EmailField(verbose_name="Correo de contacto")
    telefono = models.CharField(max_length=30, verbose_name="Teléfono")

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
    peso_kg = models.DecimalField(max_digits=7, decimal_places=1, verbose_name="Peso (kg)")
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
    ubicacion = models.CharField(max_length=150, verbose_name="Ubicación")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    capacidad = models.PositiveIntegerField()

    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Bodegas"

    def __str__(self):
        return self.nombre


class Vehiculo(models.Model):
    TIPO_CAMION = "camion"
    TIPO_VAN = "van"
    TIPO_TRAILER = "trailer"
    TIPO_CHOICES = [
        (TIPO_CAMION, "Camión"),
        (TIPO_VAN, "Van"),
        (TIPO_TRAILER, "Tráiler"),
    ]

    patente = models.CharField(max_length=10, unique=True, verbose_name="Patente")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    capacidad_kg = models.DecimalField(max_digits=8, decimal_places=1, verbose_name="Capacidad (kg)")
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name="vehiculos")

    class Meta:
        ordering = ["patente"]

    def __str__(self):
        return self.patente


class Conductor(models.Model):
    nombre = models.CharField(max_length=150)
    licencia = models.CharField(max_length=30, unique=True, verbose_name="Licencia")
    telefono = models.CharField(max_length=30, verbose_name="Teléfono")
    vehiculo = models.ForeignKey(
        Vehiculo, on_delete=models.SET_NULL, related_name="conductores", null=True, blank=True
    )

    class Meta:
        ordering = ["nombre"]

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

    codigo = models.CharField(max_length=30, unique=True, verbose_name="Código")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name="envios")
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name="envios")
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="envios")
    vehiculo = models.ForeignKey(
        Vehiculo, on_delete=models.SET_NULL, related_name="envios", null=True, blank=True
    )
    conductor = models.ForeignKey(
        Conductor, on_delete=models.SET_NULL, related_name="envios", null=True, blank=True
    )
    destino = models.CharField(max_length=200)
    peso_total_kg = models.DecimalField(max_digits=7, decimal_places=1, verbose_name="Peso total (kg)")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_PREPARANDO)
    fecha_envio = models.DateField(verbose_name="Fecha de envío")
    fecha_estimada_entrega = models.DateField(verbose_name="Fecha estimada de entrega")
    fecha_real_entrega = models.DateField(null=True, blank=True, verbose_name="Fecha real de entrega")
    ubicacion_actual = models.CharField(max_length=200, verbose_name="Ubicación actual")

    class Meta:
        ordering = ["-fecha_envio"]

    def __str__(self):
        return self.codigo


class SeguimientoEvento(models.Model):
    envio = models.ForeignKey(Envio, on_delete=models.CASCADE, related_name="eventos")
    descripcion = models.CharField(max_length=255, verbose_name="Descripción")
    ubicacion = models.CharField(max_length=200, verbose_name="Ubicación")
    fecha_hora = models.DateTimeField(verbose_name="Fecha y hora")

    class Meta:
        ordering = ["fecha_hora"]
        verbose_name = "Evento de seguimiento"
        verbose_name_plural = "Eventos de seguimiento"

    def __str__(self):
        return f"{self.envio.codigo} · {self.descripcion}"


class Incidencia(models.Model):
    TIPO_RETRASO = "retraso"
    TIPO_DESVIO = "desvio"
    TIPO_FALLA_MECANICA = "falla_mecanica"
    TIPO_OTRO = "otro"
    TIPO_CHOICES = [
        (TIPO_RETRASO, "Retraso"),
        (TIPO_DESVIO, "Desvío"),
        (TIPO_FALLA_MECANICA, "Falla mecánica"),
        (TIPO_OTRO, "Otro"),
    ]

    envio = models.ForeignKey(Envio, on_delete=models.CASCADE, related_name="incidencias")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.CharField(max_length=255, verbose_name="Descripción")
    fecha_hora = models.DateTimeField(verbose_name="Fecha y hora")

    class Meta:
        ordering = ["-fecha_hora"]
        verbose_name = "Incidencia"
        verbose_name_plural = "Incidencias"

    def __str__(self):
        return f"{self.envio.codigo} · {self.get_tipo_display()}"


class ComprobanteEntrega(models.Model):
    envio = models.OneToOneField(Envio, on_delete=models.CASCADE, related_name="comprobante")
    nombre_receptor = models.CharField(max_length=150, verbose_name="Nombre del receptor")
    firma_url = models.CharField(max_length=300, blank=True, verbose_name="Firma digital (URL/archivo)")
    foto_url = models.CharField(max_length=300, blank=True, verbose_name="Foto de la mercadería (URL/archivo)")
    codigo_escaneado = models.CharField(max_length=100, blank=True, verbose_name="Código QR/barras escaneado")
    fecha_hora = models.DateTimeField(verbose_name="Fecha y hora de entrega")

    class Meta:
        ordering = ["-fecha_hora"]
        verbose_name = "Comprobante de entrega"
        verbose_name_plural = "Comprobantes de entrega"

    def __str__(self):
        return f"Comprobante · {self.envio.codigo}"
