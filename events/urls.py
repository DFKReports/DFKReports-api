from django.urls import path

from . import views

urlpatterns = [
    path('<wallet_hash>/', views.IncomeExpensesView, name='incomeexpensesview'),
]