from django.urls import path,include
from .views import ElevatorViewSet
from rest_framework.routers import DefaultRouter

elevator_router = DefaultRouter()
elevator_router.register(r'elevators',ElevatorViewSet)

urlpatterns = [
    path('',include(elevator_router.urls))
]