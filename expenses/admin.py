# expenses/admin.py

from django.contrib import admin
from .models import Category, Expense


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("description", "amount", "date", "time", "category", "user")
    list_filter = ("category", "date", "user")
    search_fields = ("description",)
    date_hierarchy = "date"

# Register your models here.
