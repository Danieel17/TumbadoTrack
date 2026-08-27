# TumbadoTrack

Módulo de **Transporte / Courier** de *Music Pro Company*, desarrollado para el ramo de Programación Back End (Django) — INACAP, Ingeniería en Ciberseguridad.

TumbadoTrack gestiona el transporte y seguimiento de equipos musicales (instrumentos, sonido, iluminación) para el **Tour 2026 de Natanael Cano** por México y Estados Unidos, desde proveedores internacionales hasta los recintos del tour.

## Etapas del proyecto

| Unidad | Contenido | Estado |
|---|---|---|
| 1 | Django sin base de datos, datos en diccionarios Python, Django Templates | ✅ En desarrollo |
| 2 | ORM de Django, base de datos SQLite, Django Admin, CRUD completo | ⏳ Pendiente |
| 3 | API REST con Django REST Framework + autenticación JWT | ⏳ Pendiente |

## Stack

- Python + Django
- SQLite (a partir de la Unidad 2)
- Tailwind CSS (vía CDN) para los templates
- python-decouple para variables de entorno

## Cómo levantar el proyecto (Unidad 1)

1. Clonar el repositorio y entrar a la carpeta del proyecto.

2. Crear y activar el entorno virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Copiar el archivo de variables de entorno de ejemplo:

   ```bash
   cp .env.example .env
   ```

   Editar `.env` y definir tu propio `SECRET_KEY` (por ejemplo generándolo con `django-admin startproject` en un directorio temporal, o con `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`).

5. Levantar el servidor de desarrollo:

   ```bash
   python manage.py runserver
   ```

6. Abrir [http://127.0.0.1:8000/](http://127.0.0.1:8000/) en el navegador.

> En la Unidad 1 no se usa base de datos: no es necesario correr `migrate` todavía. Los datos de ejemplo (proveedores, clientes, productos, envíos y eventos de seguimiento) están en `courier/data/seed_data.py`.

## Estructura del proyecto

```
config/                # Configuración del proyecto Django (settings, urls raíz)
courier/                # App principal: módulo de transporte/courier
    data/
        seed_data.py    # "Modelos" de la Unidad 1: listas de diccionarios
        repository.py   # Capa de acceso a datos (imita al ORM de Django)
    templates/
        courier/        # Templates propios de la app
        partials/       # Fragmentos reutilizables (ej: badge de estado)
    static/courier/      # CSS/imágenes propios de la app
    views.py
    urls.py
    models.py           # Vacío por ahora; se completa en la Unidad 2
.env                    # Variables de entorno locales (no se sube a git)
.env.example            # Plantilla de variables de entorno
```

## Roadmap técnico (para no reescribir en unidades futuras)

- **Unidad 2:** los diccionarios de `seed_data.py` se migran a modelos reales en `models.py` (Proveedor, Cliente, Producto, Envio, SeguimientoEvento, Bodega) con las mismas relaciones y nombres de campo. Se agregan migraciones, `admin.py` y vistas CRUD.
- **Unidad 3:** se agrega Django REST Framework con serializers y ViewSets dentro de la app `courier`, autenticación JWT con `djangorestframework-simplejwt`, y rutas expuestas bajo `/api/`.

La app `courier` está pensada como módulo independiente para poder integrarse a futuro, vía API REST, con los otros módulos del sistema Music Pro Company (bodega principal, sucursales/franquicias, pagos).
