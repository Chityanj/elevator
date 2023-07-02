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
        num_elevators = request.data.get('num_elevators')
        if not num_elevators or not isinstance(num_elevators,int):
            return Response({"error": "Please provide the number of elevators to initialize the system"},status=status.HTTP_400_BAD_REQUEST)
        Elevator.objects.all().delete() # Delete all elevators if exists

        elevators = []
        for _ in range(num_elevators):
            elevator= Elevator.objects.create()
            elevators.append({'elevator_id': elevator.pk})

        return Response({"message": f"{num_elevators} elevators initialized successfully.","elevators": elevators},status=status.HTTP_200_OK) 
    
    @action(detail=True, methods=['get'])
    def get_elevator_details(self, request, pk=None):
        """
        API to fetch details about a specific elevator
        """
        elevator = self.get_object()
        serializer = self.get_serializer(elevator)
        return Response(serializer.data, status=status.HTTP_200_OK)