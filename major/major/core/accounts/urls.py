from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('patient/<int:patient_id>/reports/', views.patient_reports, name='patient_reports'),
    path('patient/<int:patient_id>/add-report/', views.add_report, name='add_report'),
    path('upload-report/', views.report_upload, name='report_upload'),
    path('reports/<str:name>/', views.reports_by_patient, name='reports_by_patient'),
    path('iv-dashboard/', views.iv_dashboard, name='iv_dashboard'),
]

  






