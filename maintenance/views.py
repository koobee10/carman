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
from .models import MaintenanceRecord, MaintenanceSchedule
from .forms import MaintenanceRecordForm, MaintenanceScheduleForm
from vehicles.models import Vehicle
from django.utils import timezone
from django.db.models import Sum

# MaintenanceRecord Views
class MaintenanceRecordListView(LoginRequiredMixin, ListView):
    model = MaintenanceRecord
    template_name = 'maintenance/record_list.html'
    context_object_name = 'records'
    ordering = ['-date']
    
    def get_queryset(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        if vehicle_id:
            vehicle = get_object_or_404(Vehicle, id=vehicle_id, owner=self.request.user)
            return MaintenanceRecord.objects.filter(vehicle=vehicle).order_by('-date')
        else:
            return MaintenanceRecord.objects.filter(vehicle__owner=self.request.user).order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle_id = self.kwargs.get('vehicle_id')
        if vehicle_id:
            context['vehicle'] = get_object_or_404(Vehicle, id=vehicle_id, owner=self.request.user)
        
        # Calculate maintenance metrics
        records = self.get_queryset()
        context['record_count'] = records.count()
        
        # Get latest service date
        if records.exists():
            context['last_service_date'] = records.order_by('-date').first().date
        
        # Calculate total maintenance costs
        context['total_spent'] = records.aggregate(Sum('cost'))['cost__sum'] or 0
        
        return context

class MaintenanceRecordDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = MaintenanceRecord
    template_name = 'maintenance/record_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        record = self.get_object()
        # Add debug information
        print(f"DEBUG: Record ID: {record.id}, Record: {record}")
        if record.vehicle:
            print(f"DEBUG: Vehicle ID: {record.vehicle.id}, Vehicle: {record.vehicle}")
        else:
            print("DEBUG: No vehicle associated with this record")
        return context
    
    def test_func(self):
        record = self.get_object()
        if not record.vehicle or not record.vehicle.owner:
            return False
        return self.request.user == record.vehicle.owner

class MaintenanceRecordCreateView(LoginRequiredMixin, CreateView):
    model = MaintenanceRecord
    form_class = MaintenanceRecordForm
    template_name = 'maintenance/record_form.html'
    
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
    
    def form_valid(self, form):
        # Add debug logging
        vehicle = form.cleaned_data.get('vehicle')
        if vehicle:
            print(f"DEBUG: Saving record with vehicle: {vehicle.id} - {vehicle.nickname}")
        else:
            print("DEBUG: No vehicle selected in the form")
        return super().form_valid(form)
        
    def get_success_url(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        if vehicle_id:
            return f'/maintenance/records/vehicle/{vehicle_id}/'
        return '/maintenance/records/'

class MaintenanceRecordUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MaintenanceRecord
    form_class = MaintenanceRecordForm
    template_name = 'maintenance/record_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def test_func(self):
        record = self.get_object()
        if not record.vehicle or not record.vehicle.owner:
            return False
        return self.request.user == record.vehicle.owner

class MaintenanceRecordDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MaintenanceRecord
    template_name = 'maintenance/record_confirm_delete.html'
    
    def get_success_url(self):
        record = self.get_object()
        if not record.vehicle:
            return '/maintenance/records/'
        return f'/maintenance/records/vehicle/{record.vehicle.id}/'
    
    def test_func(self):
        record = self.get_object()
        if not record.vehicle or not record.vehicle.owner:
            return False
        return self.request.user == record.vehicle.owner

# MaintenanceSchedule Views
class MaintenanceScheduleListView(LoginRequiredMixin, ListView):
    model = MaintenanceSchedule
    template_name = 'maintenance/schedule_list.html'
    context_object_name = 'schedules'
    
    def get_queryset(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        if vehicle_id:
            vehicle = get_object_or_404(Vehicle, id=vehicle_id, owner=self.request.user)
            return MaintenanceSchedule.objects.filter(vehicle=vehicle)
        else:
            return MaintenanceSchedule.objects.filter(vehicle__owner=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle_id = self.kwargs.get('vehicle_id')
        if vehicle_id:
            context['vehicle'] = get_object_or_404(Vehicle, id=vehicle_id, owner=self.request.user)
        
        # Add due schedules
        schedules = self.get_queryset()
        due_schedules = []
        today = timezone.now().date()
        
        for schedule in schedules:
            if schedule.interval_type in ['date', 'both'] and schedule.next_service_date:
                if schedule.next_service_date <= today:
                    due_schedules.append(schedule)
            
        context['due_schedules'] = due_schedules
        return context

class MaintenanceScheduleDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = MaintenanceSchedule
    template_name = 'maintenance/schedule_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schedule = self.get_object()
        # Add some debug information
        if schedule.vehicle:
            print(f"DEBUG: Vehicle ID: {schedule.vehicle.id}, Vehicle: {schedule.vehicle}")
        else:
            print("DEBUG: No vehicle associated with this schedule")
        return context
    
    def test_func(self):
        schedule = self.get_object()
        if not schedule.vehicle or not schedule.vehicle.owner:
            return False
        return self.request.user == schedule.vehicle.owner

class MaintenanceScheduleCreateView(LoginRequiredMixin, CreateView):
    model = MaintenanceSchedule
    form_class = MaintenanceScheduleForm
    template_name = 'maintenance/schedule_form.html'
    
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
    
    def form_valid(self, form):
        # Add debug logging
        vehicle = form.cleaned_data.get('vehicle')
        if vehicle:
            print(f"DEBUG: Saving schedule with vehicle: {vehicle.id} - {vehicle.nickname}")
        else:
            print("DEBUG: No vehicle selected in the form")
        return super().form_valid(form)
    
    def get_success_url(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        if vehicle_id:
            return f'/maintenance/schedules/vehicle/{vehicle_id}/'
        return '/maintenance/schedules/'

class MaintenanceScheduleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MaintenanceSchedule
    form_class = MaintenanceScheduleForm
    template_name = 'maintenance/schedule_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def test_func(self):
        schedule = self.get_object()
        if not schedule.vehicle or not schedule.vehicle.owner:
            return False
        return self.request.user == schedule.vehicle.owner
    
    def get_success_url(self):
        schedule = self.get_object()
        if not schedule.vehicle:
            return '/maintenance/schedules/'
        return f'/maintenance/schedules/vehicle/{schedule.vehicle.id}/'

class MaintenanceScheduleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MaintenanceSchedule
    template_name = 'maintenance/schedule_confirm_delete.html'
    
    def get_success_url(self):
        schedule = self.get_object()
        if not schedule.vehicle:
            return '/maintenance/schedules/'
        return f'/maintenance/schedules/vehicle/{schedule.vehicle.id}/'
    
    def test_func(self):
        schedule = self.get_object()
        if not schedule.vehicle or not schedule.vehicle.owner:
            return False
        return self.request.user == schedule.vehicle.owner
