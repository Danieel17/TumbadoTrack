from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
