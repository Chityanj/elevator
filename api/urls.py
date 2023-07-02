from django.urls import path,include
from api.views import ElevatorViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'elevators',ElevatorViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('initialize_system/', ElevatorViewSet.as_view({'post': 'initialize_system'}), name='initialize_system'),
    path('<int:pk>/get_elevator_details/', ElevatorViewSet.as_view({'get': 'get_elevator_details'}), name='get_elevator_details'),
] 