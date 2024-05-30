from django.urls import path
from . import views

urlpatterns = [
    # ユーザー詳細
    path("users/<uid>/", views.UserDetailView.as_view()),
]
