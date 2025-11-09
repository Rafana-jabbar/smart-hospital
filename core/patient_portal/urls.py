from django.urls import path
from . import views


app_name = 'patient_portal'

urlpatterns = [
    path('login/', views.patient_login, name='login'),
    # path('register/', views.patient_register, name='register'),
    path('logout/', views.patient_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reports/download/<int:report_id>/', views.download_report, name='download_report'),
    path('appointments/book/', views.book_appointment, name='book_appointment'),
    path('appointments/', views.appointment_history, name='appointments'),
]


