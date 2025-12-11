from django.urls import path
from .views import expense_list

urlpatterns = [
    path('', expense_list, name='expense_list'),
]
# mytracker/urls.py
from django.contrib import admin
from django.urls import path, include
from expenses import views as expense_views

urlpatterns = [
    
    # home pubblica
    path('', expense_views.home, name='home'),

    # dashboard / lista spese (solo loggati)
    path('app/', expense_views.expense_list, name='expense_list'),
]
