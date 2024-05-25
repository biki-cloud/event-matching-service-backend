from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.EventView.as_view()),
    path('events/<int:id>/', views.EventView.as_view()),
]