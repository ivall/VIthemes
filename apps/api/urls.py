from django.urls import path
from . import views

urlpatterns = [
    path('themes/<uuid:pk>/', views.ThemeView.as_view(), name='theme_view'),
]