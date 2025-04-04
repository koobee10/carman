from django.urls import path
from . import views
from .views import (
    VehicleListView,
    VehicleDetailView,
    VehicleCreateView,
    VehicleUpdateView,
    VehicleDeleteView
)

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('vehicles/', VehicleListView.as_view(), name='vehicle-list'),
    path('vehicle/<int:pk>/', VehicleDetailView.as_view(), name='vehicle-detail'),
    path('vehicle/new/', VehicleCreateView.as_view(), name='vehicle-create'),
    path('vehicle/<int:pk>/update/', VehicleUpdateView.as_view(), name='vehicle-update'),
    path('vehicle/<int:pk>/delete/', VehicleDeleteView.as_view(), name='vehicle-delete'),
    path('vehicle/<int:pk>/add_image/', views.add_vehicle_image, name='add-vehicle-image'),
    path('vehicle/<int:pk>/manage_images/', views.manage_vehicle_images, name='manage-vehicle-images'),
    path('vehicle/<int:vehicle_pk>/delete_image/<int:image_pk>/', views.delete_vehicle_image, name='delete-vehicle-image'),
    path('vehicle/<int:vehicle_pk>/set_primary_image/<int:image_pk>/', views.set_primary_image, name='set-primary-image'),
    path('vehicle/<int:pk>/update_mileage/', views.update_mileage, name='update-mileage'),
] 