from django.urls import path
from . import views


app_name = 'doctor_portal'

urlpatterns = [
    path('login/', views.doctor_login, name='login'),
    path('logout/', views.doctor_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('patients/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('appointments/<int:appointment_id>/approve/', views.approve_appointment, name='approve_appointment'),
    path('appointments/<int:appointment_id>/reject/', views.reject_appointment, name='reject_appointment'),
    path('patients/<int:patient_id>/add-note/', views.add_note, name='add_note'),
]


