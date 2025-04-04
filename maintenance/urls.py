from django.urls import path
from . import views
from .views import (
    MaintenanceRecordListView,
    MaintenanceRecordDetailView,
    MaintenanceRecordCreateView,
    MaintenanceRecordUpdateView,
    MaintenanceRecordDeleteView,
    MaintenanceScheduleListView,
    MaintenanceScheduleDetailView,
    MaintenanceScheduleCreateView,
    MaintenanceScheduleUpdateView,
    MaintenanceScheduleDeleteView
)

urlpatterns = [
    # Maintenance Records URLs
    path('records/', MaintenanceRecordListView.as_view(), name='maintenance-record-list'),
    path('records/vehicle/<int:vehicle_id>/', MaintenanceRecordListView.as_view(), name='vehicle-maintenance-records'),
    path('records/<int:pk>/', MaintenanceRecordDetailView.as_view(), name='maintenance-record-detail'),
    path('records/new/', MaintenanceRecordCreateView.as_view(), name='maintenance-record-create'),
    path('records/new/vehicle/<int:vehicle_id>/', MaintenanceRecordCreateView.as_view(), name='maintenance-record-create-for-vehicle'),
    path('records/new/schedule/<int:schedule_id>/', MaintenanceRecordCreateView.as_view(), name='maintenance-record-create-from-schedule'),
    path('records/<int:pk>/update/', MaintenanceRecordUpdateView.as_view(), name='maintenance-record-update'),
    path('records/<int:pk>/delete/', MaintenanceRecordDeleteView.as_view(), name='maintenance-record-delete'),
    
    # Maintenance Schedules URLs
    path('schedules/', MaintenanceScheduleListView.as_view(), name='maintenance-schedule-list'),
    path('schedules/vehicle/<int:vehicle_id>/', MaintenanceScheduleListView.as_view(), name='vehicle-maintenance-schedules'),
    path('schedules/<int:pk>/', MaintenanceScheduleDetailView.as_view(), name='maintenance-schedule-detail'),
    path('schedules/new/', MaintenanceScheduleCreateView.as_view(), name='maintenance-schedule-create'),
    path('schedules/new/vehicle/<int:vehicle_id>/', MaintenanceScheduleCreateView.as_view(), name='maintenance-schedule-create-for-vehicle'),
    path('schedules/<int:pk>/update/', MaintenanceScheduleUpdateView.as_view(), name='maintenance-schedule-update'),
    path('schedules/<int:pk>/delete/', MaintenanceScheduleDeleteView.as_view(), name='maintenance-schedule-delete'),
] 