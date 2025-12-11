from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Expense

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label="Nome", max_length=30, required=True)
    last_name = forms.CharField(label="Cognome", max_length=30, required=True)
    email = forms.EmailField(label="Email", required=True)
    reason = forms.CharField(
        label="Perché vuoi usare MyTracker?",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Testo di aiuto più semplice
        self.fields["username"].help_text = "Puoi usare anche la tua email."
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

        # Stessa classe Tailwind per tutti i campi input/textarea
        base_classes = (
            "w-full bg-white border border-gray-300 rounded-lg px-4 py-2.5 "
            "focus:ring-2 focus:ring-blue-500 focus:border-blue-500 "
            "outline-none transition"
        )
        for name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.PasswordInput)):
                field.widget.attrs.update({"class": base_classes})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({"class": base_classes + " resize-none"})

    # Messaggio di errore password unico e più corto
    def clean_password1(self):
        pwd = self.cleaned_data.get("password1")
        if pwd:
            try:
                validate_password(pwd, self.instance)
            except ValidationError:
                raise ValidationError(
                    "La password non rispetta i requisiti minimi "
                    "(almeno 8 caratteri, non troppo comune, non solo numeri)."
                )
        return pwd

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["date", "time", "category", "description", "amount"]
