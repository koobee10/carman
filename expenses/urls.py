from django.urls import path
from . import views
from .views import (
    ExpenseListView,
    ExpenseDetailView,
    ExpenseCreateView,
    ExpenseUpdateView,
    ExpenseDeleteView
)

urlpatterns = [
    path('', ExpenseListView.as_view(), name='expense-list'),
    path('vehicle/<int:vehicle_id>/', ExpenseListView.as_view(), name='vehicle-expenses'),
    path('<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),
    path('new/', ExpenseCreateView.as_view(), name='expense-create'),
    path('new/vehicle/<int:vehicle_id>/', ExpenseCreateView.as_view(), name='expense-create-for-vehicle'),
    path('<int:pk>/update/', ExpenseUpdateView.as_view(), name='expense-update'),
    path('<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense-delete'),
    path('<int:expense_id>/add_receipt/', views.add_receipt, name='add-receipt'),
] 