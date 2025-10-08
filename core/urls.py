from django.urls import path
from . import views

urlpatterns = [
    # This path matches the root URL (e.g., http://127.0.0.1:8000/) 
    # and points to the home_view function.
    path('', views.home_view, name='home'), 
    
    # This path handles the dashboard viewing logic.
    path('parent/<str:parent_email>/', views.parent_dashboard_view, name='parent_dashboard'),
]
