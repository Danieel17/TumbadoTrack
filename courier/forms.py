from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Cliente, Envio, Proveedor

TEXT_INPUT_CLASSES = (
    "w-full rounded-md border border-stone-300 dark:border-stone-600 bg-stone-50 dark:bg-stone-700 "
    "text-stone-900 dark:text-stone-100 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal-400"
)
CHECKBOX_CLASSES = "rounded border-stone-300 text-teal-500 focus:ring-teal-400"


class EstiloFormMixin:
    """Aplica las clases Tailwind del sitio a todos los campos del formulario."""

    campos_checkbox = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for nombre, campo in self.fields.items():
            if nombre in self.campos_checkbox:
                campo.widget.attrs.setdefault("class", CHECKBOX_CLASSES)
            else:
                campo.widget.attrs.setdefault("class", TEXT_INPUT_CLASSES)


class ProveedorForm(EstiloFormMixin, forms.ModelForm):
    campos_checkbox = ("activo",)

    class Meta:
        model = Proveedor
        fields = ["nombre", "pais", "email_contacto", "telefono", "tasa_puntualidad", "activo"]


class ClienteForm(EstiloFormMixin, forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "ciudad", "tipo", "email_contacto", "telefono"]


class EnvioForm(EstiloFormMixin, forms.ModelForm):
    class Meta:
        model = Envio
        fields = [
            "codigo", "producto", "proveedor", "cliente", "destino",
            "peso_total_kg", "estado", "fecha_envio", "fecha_estimada_entrega",
            "fecha_real_entrega", "ubicacion_actual",
        ]
        widgets = {
            "fecha_envio": forms.DateInput(attrs={"type": "date"}),
            "fecha_estimada_entrega": forms.DateInput(attrs={"type": "date"}),
            "fecha_real_entrega": forms.DateInput(attrs={"type": "date"}),
        }


class UsuarioCreationForm(UserCreationForm):
    """Alta de usuarios desde el panel de administración del sitio (no el /admin/ de Django)."""

    email = forms.EmailField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "first_name", "last_name", "email", "is_staff", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for nombre in self.fields:
            self.fields[nombre].widget.attrs.setdefault(
                "class",
                "w-full rounded-md border border-stone-300 dark:border-stone-600 bg-stone-50 dark:bg-stone-700 "
                "text-stone-900 dark:text-stone-100 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal-400",
            )
        self.fields["is_staff"].widget.attrs["class"] = "rounded border-stone-300 text-teal-500 focus:ring-teal-400"
        self.fields["is_active"].widget.attrs["class"] = "rounded border-stone-300 text-teal-500 focus:ring-teal-400"


class UsuarioEditForm(forms.ModelForm):
    """Edición de datos y rol de un usuario existente, sin tocar la contraseña."""

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "is_staff", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for nombre in self.fields:
            self.fields[nombre].widget.attrs.setdefault(
                "class",
                "w-full rounded-md border border-stone-300 dark:border-stone-600 bg-stone-50 dark:bg-stone-700 "
                "text-stone-900 dark:text-stone-100 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal-400",
            )
        self.fields["is_staff"].widget.attrs["class"] = "rounded border-stone-300 text-teal-500 focus:ring-teal-400"
        self.fields["is_active"].widget.attrs["class"] = "rounded border-stone-300 text-teal-500 focus:ring-teal-400"
