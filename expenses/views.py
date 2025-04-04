from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from django.db.models import Sum, F
from .models import Expense, Receipt
from .forms import ExpenseForm, ReceiptForm
from vehicles.models import Vehicle
from django.http import JsonResponse

class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'
    ordering = ['-date']
    
    def get_queryset(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        if vehicle_id:
            vehicle = get_object_or_404(Vehicle, id=vehicle_id, owner=self.request.user)
            return Expense.objects.filter(vehicle=vehicle).order_by('-date')
        else:
            return Expense.objects.filter(vehicle__owner=self.request.user).order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle_id = self.kwargs.get('vehicle_id')
        if vehicle_id:
            context['vehicle'] = get_object_or_404(Vehicle, id=vehicle_id, owner=self.request.user)
        
        # Calculate totals
        expenses = self.get_queryset()
        total = expenses.aggregate(
            total=Sum(F('amount') + F('tax') + F('shipping') + F('labor_cost'))
        )['total'] or 0
        
        # Set values for display in template
        context['total_amount'] = total
        context['total_spent'] = total
        context['expense_count'] = expenses.count()
        context['average_expense'] = total / context['expense_count'] if context['expense_count'] > 0 else 0
        
        # Category breakdown
        context['category_totals'] = expenses.values('category').annotate(
            total=Sum(F('amount') + F('tax') + F('shipping') + F('labor_cost'))
        ).order_by('-total')
        
        return context

class ExpenseDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Expense
    
    def test_func(self):
        expense = self.get_object()
        return self.request.user == expense.vehicle.owner

class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_initial(self):
        initial = super().get_initial()
        vehicle_id = self.kwargs.get('vehicle_id')
        if vehicle_id:
            initial['vehicle'] = get_object_or_404(Vehicle, id=vehicle_id, owner=self.request.user)
        return initial

class ExpenseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def test_func(self):
        expense = self.get_object()
        return self.request.user == expense.vehicle.owner

class ExpenseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Expense
    
    def get_success_url(self):
        expense = self.get_object()
        return f'/expenses/vehicle/{expense.vehicle.id}/'
    
    def test_func(self):
        expense = self.get_object()
        return self.request.user == expense.vehicle.owner

@login_required
def add_receipt(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, vehicle__owner=request.user)
    
    if request.method == 'POST':
        form = ReceiptForm(request.POST, request.FILES)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.expense = expense
            receipt.save()
            messages.success(request, 'Receipt added successfully!')
            return redirect('expense-detail', pk=expense.id)
    else:
        form = ReceiptForm()
    
    return render(request, 'expenses/add_receipt.html', {'form': form, 'expense': expense})

@login_required
def get_expenses_by_vehicle(request, vehicle_id):
    """API endpoint to get expenses for a specific vehicle"""
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, owner=request.user)
    expenses = Expense.objects.filter(vehicle=vehicle).order_by('-date')
    
    expense_data = []
    for expense in expenses:
        expense_data.append({
            'id': expense.id,
            'date': expense.date.strftime('%Y-%m-%d'),
            'description': expense.description,
            'amount': float(expense.amount),
            'category': expense.category,
        })
    
    return JsonResponse(expense_data, safe=False)
