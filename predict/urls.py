# predict/urls.py
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from churn_app.views import make_prediction  # Correct app name
  # Replace 'myapp' with your actual app name

def home(request):
    return HttpResponse("<h1>Welcome to the Churn Prediction App</h1>")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # This adds a homepage
    path('predict/', make_prediction, name='make_prediction'),
]

