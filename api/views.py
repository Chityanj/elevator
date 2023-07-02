from django.shortcuts import render
from rest_framework.decorators import action
from api.models import Elevator
from api.serializers import ElevatorSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response

# Create your views here.
class ElevatorViewSet(viewsets.ModelViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

    @action(detail=False, methods=['post'])
    def initialize_system(self,request):
        num_elevators = request.data.get['num_elevators']
        if not num_elevators or not isinstance(num_elevators,int):
            return Response({"error": "Please provide the number of elevators to initialize the system"},status=status.HTTP_400_BAD_REQUEST)
        Elevator.objects.all().delete() # Delete all elevators if exists

        for i in range(num_elevators):
            Elevator.objects.create()

        return Response({"message": f"{num_elevators} elevators initialized successfully"},status=status.HTTP_200_OK) 