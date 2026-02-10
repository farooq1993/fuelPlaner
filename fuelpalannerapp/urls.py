from django.urls import path
from . import views

urlpatterns = [
    path("route/", views.RouteFuelAPIView.as_view()),
]