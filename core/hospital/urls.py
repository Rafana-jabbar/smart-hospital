from django.urls import path
from hospital import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('patient/', views.patient, name='patient'),
    # path('doctor/', views.doctor, name='doctor'),
    path('admin/', views.admin_portal, name='admin'),
]
