# expenses/forms.py
from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['date', 'time', 'description', 'category', 'amount']
        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'time': forms.TimeInput(
                attrs={'type': 'time'}
            ),
        }
