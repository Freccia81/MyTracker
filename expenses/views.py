# expenses/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .forms import ExpenseForm
from .models import Expense

def home(request):
    # se è già loggato lo mando direttamente alla dashboard
    if request.user.is_authenticated:
        return redirect('expense_list')
    return render(request, 'home.html')  # nuovo template

@login_required
def expense_list(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()

    today = date.today()
    expenses = Expense.objects.filter(
        user=request.user,
        date__year=today.year,
        date__month=today.month,
    )

    month_total = expenses.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'form': form,
        'expenses': expenses,
        'month_total': month_total,
    }

    return render(request, 'expenses/expense_list.html', context)
    #                       ^^^^^^^^^^^^^^^^^^^^^^^^^
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login automatico dopo la registrazione
            login(request, user)
            return redirect('expense_list')  # vai subito alla tua app
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})