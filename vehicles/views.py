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
from .models import Vehicle, VehicleImage
from .forms import VehicleForm, VehicleImageForm

@login_required
def dashboard(request):
    vehicles = Vehicle.objects.filter(owner=request.user).order_by('-date_added')
    return render(request, 'vehicles/dashboard.html', {'vehicles': vehicles})

class VehicleListView(LoginRequiredMixin, ListView):
    model = Vehicle
    template_name = 'vehicles/vehicle_list.html'
    context_object_name = 'vehicles'
    ordering = ['-date_added']
    
    def get_queryset(self):
        return Vehicle.objects.filter(owner=self.request.user)

class VehicleDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Vehicle
    
    def test_func(self):
        vehicle = self.get_object()
        return self.request.user == vehicle.owner

class VehicleCreateView(LoginRequiredMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class VehicleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Vehicle
    form_class = VehicleForm
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, f"Error updating vehicle: {form.errors}")
        return super().form_invalid(form)
    
    def test_func(self):
        vehicle = self.get_object()
        return self.request.user == vehicle.owner

class VehicleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Vehicle
    success_url = '/'
    
    def test_func(self):
        vehicle = self.get_object()
        return self.request.user == vehicle.owner

@login_required
def add_vehicle_image(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = VehicleImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.vehicle = vehicle
            image.save()
            messages.success(request, f'Image added to {vehicle.nickname}!')
            return redirect('vehicle-detail', pk=vehicle.pk)
    else:
        form = VehicleImageForm()
    
    return render(request, 'vehicles/add_image.html', {'form': form, 'vehicle': vehicle})

@login_required
def update_mileage(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        new_mileage = request.POST.get('mileage')
        if new_mileage:
            current_mileage = vehicle.mileage if hasattr(vehicle, 'mileage') else 0
            if int(new_mileage) >= current_mileage:
                vehicle.mileage = new_mileage
                vehicle.save()
                messages.success(request, f'Mileage updated for {vehicle.nickname}!')
                return redirect('vehicle-detail', pk=vehicle.pk)
            else:
                messages.error(request, 'New mileage must be greater than or equal to the current mileage.')
    
    return render(request, 'vehicles/update_mileage.html', {'vehicle': vehicle})

@login_required
def manage_vehicle_images(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, owner=request.user)
    images = vehicle.images.all()
    
    return render(request, 'vehicles/manage_images.html', {'vehicle': vehicle, 'images': images})

@login_required
def delete_vehicle_image(request, vehicle_pk, image_pk):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_pk, owner=request.user)
    image = get_object_or_404(VehicleImage, pk=image_pk, vehicle=vehicle)
    
    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Image deleted successfully!')
        return redirect('manage-vehicle-images', pk=vehicle.pk)
    
    return render(request, 'vehicles/delete_image_confirm.html', {'vehicle': vehicle, 'image': image})

@login_required
def set_primary_image(request, vehicle_pk, image_pk):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_pk, owner=request.user)
    image = get_object_or_404(VehicleImage, pk=image_pk, vehicle=vehicle)
    
    if request.method == 'POST':
        # Update is_primary flag
        image.is_primary = True
        image.save()  # The model's save method will handle unsetting other primary images
        messages.success(request, 'Primary image updated successfully!')
        return redirect('manage-vehicle-images', pk=vehicle.pk)
    
    return redirect('manage-vehicle-images', pk=vehicle.pk)
