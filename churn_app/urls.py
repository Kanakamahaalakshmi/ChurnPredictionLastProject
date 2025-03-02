from django.urls import path
from . import views  # Import views from your app

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('predict/', views.make_prediction, name='make_prediction'),  # Prediction endpoint
    path('export-csv/', views.export_churn_csv, name='export_csv'),  # Export to CSV
]
