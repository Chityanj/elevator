from django.shortcuts import render
from rest_framework.decorators import action
from api.models import Elevator, Request
from api.serializers import ElevatorSerializer, RequestSerializer
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
    
    @action(detail=False, methods=['post'])
    def save_request(self, request, pk=None):
        """
        API to save a user request to the list of requests for an elevator
        and determine the direction to move the elevator based on the requested floor
        """
        elevator_id = request.data.get('elevator_id')
        elevator = Elevator.objects.get(pk=elevator_id)
        floor = request.data.get('floor')

        if not floor or not isinstance(floor, int) or floor <= 0:
            return Response({'error': 'Invalid floor number provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if elevator.in_maintenance:
            return Response({'error': 'Elevator is in maintenance.'}, status=status.HTTP_400_BAD_REQUEST)

        if elevator.door_opened:
            return Response({'error': 'Elevator door is open.'}, status=status.HTTP_400_BAD_REQUEST)


        # Determine the direction to move the elevator
        if floor > elevator.current_floor:
            direction = 1  # Move up
        elif floor < elevator.current_floor:
            direction = -1  # Move down
        else:
            direction = 0  # Stay stationary

        # Save the request
        Request.objects.create(elevator=elevator, floor=floor)

        return Response({'message': 'User request saved successfully.',
                         'elevator_id': elevator.pk,
                         'direction': direction},
                        status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def get_requests(self, request, pk=None):
        """
        API to fetch all requests for a given elevator
        """
        try:
            elevator = self.get_object()
            requests = Request.objects.filter(elevator=elevator)
            serializer = RequestSerializer(requests, many=True)
            return Response(serializer.data)
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator not found.'}, status=status.HTTP_404_NOT_FOUND)