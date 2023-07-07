# Elevator 
Elevator System

## Installation
- Clone the Repository
```bash
git clone
cd <project dir>
```
- Install the project dependencies
```bash
pip install -r requirements.txt
```
## Run the project
- Flush the db before
```bash
python3 manage.py flush
```
- Make Migration
```bash
python3 manage.py makemigrations
```
- Migrate
```bash
python3 manage.py migrate
```
- Run Server
```bash
python3 manage.py runserver
```
## Thought Process and Design
First i thought it from the perspective of one elevator Just like implemented creating a new elevator then every elevator have its own configuration or say requests then to allocate a new elevator to a request initally i just used simple minimum distance between the elevator current floor and the new request floor but later on i thought the elevator final destination would be the floor it would be going as one elevator can have multiple requests then i calculated the distance between the elevator and the previous request to floor where it has to go for door and maintenance i used not operator to invert whatever the boolean value is 
In real world scenarios there are mainly three type of elevator 
- Full Collective: Which will assigns lifts to passengers according to the distance and the direction 
- Up collective: Which will only takes passenger requests for going up it will discard all r  equests of the passenger going down ie it priotizes going up will only go down if there are no pending requests for up or has reached the top most floor
- Down collective:Which will only takes passenger requests for going down it will discard all requests of the passenger going up ie it priotizes going down will only go up if there are no pending requests for up or has reached the down most floor

#### The System i implemented is first come first serve basis it will complete a request fully based upon created_at time it will go to to requested_from floor from the current floor then it will go to requested_to floor and mark the request as completed

## Elevator Allocation Algorithm
It is in the save_request

The algorithm first checks for the availability of elevators that are not in maintenance and have their doors closed.
If no elevators are available, it returns an error indicating that no elevators are available.
Then the system calculate the distance between the requested from floor for this new request to the last requested to floor as ultimately the elevator will be on its requested to floor after marking the request as completed and it will be its current floor 
The distances are stored in a list along with the corresponding elevator objects.
The list is sorted in ascending order based on the distances, ensuring that the elevator with the shortest distance is assigned first.
The closest elevator is selected from the sorted list, and the user request is associated with that elevator.
The request is saved in the database with the elevator and relevant floor details.

## API  Reference

### Initialize System

- URL: /api/v1/elevators/initialize_system
- Method: POST
- Description: Initialize the elevator system with a specified number of elevators.
- Request Body:
```json
{
    "num_elevators": 3
}
```
- Response:
```json
{
    "message": "3 elevators initialized successfully.",
    "elevators": [
        {"elevator_id": 1},
        {"elevator_id": 2},
        {"elevator_id": 3}
    ]
}
```
### Save Request

- URL: /api/v1/elevators/save_request
- Method: POST
- Description: Save a user request and assign the most optimal elevator to the request.
- Request Body:
```json
{
    "requested_from_floor": 3,
    "requested_to_floor": 7
}
```
- Response:
```json
{
    "message": "User request saved successfully.",
    "elevator_id": 1
}
```
### Get Requests

- URL: /api/v1/elevators/{elevator_id}/get_requests
- Method: GET
- Description: Fetch all requests for a given elevator.
- Response:
```json
[
    {
        "id": 1,
        "elevator": 1,
        "requested_from_floor": 3,
        "requested_to_floor": 7,
        "created_at": "2023-07-05T10:00:00Z",
        "is_complete": false
    },
    {
        "id": 2,
        "elevator": 1,
        "requested_from_floor": 5,
        "requested_to_floor": 2,
        "created_at": "2023-07-05T10:15:00Z",
        "is_complete": false
    }
]
```
### Get Next Floor

- URL: /api/v1/elevators/{elevator_id}/get_next_floor
- Method: GET
- Description: Fetch the next destination floor for a given elevator.
- Response:
```json

{
    "message": "Next floor retrieved successfully.",
    "elevator_id": 1,
    "next_floor": 7
}
```
### Direction

- URL: /api/v1/elevators/{elevator_id}/direction
- Method: GET
- Description: Check the direction (up, down, or stationary) of the elevator.
- Response:
```json
{
    "message": "Direction retrieved successfully.",
    "elevator_id": 1,
    "direction": "up"
}
```
### Toggle Door

- URL: /api/v1/elevators/{elevator_id}/toggle_door
- Method: POST
- Description: Toggle the door of the elevator (open or closed).
- Response:
```json

{
    "door_opened": true
}
```
### Toggle Maintenance

- URL: /api/v1/elevators/{elevator_id}/toggle_maintenance
- Method: POST
- Description: Toggle the maintenance status of an elevator.
- Response:
```json
{
    "message": "Elevator marked as in maintenance."
}
```
### Move Elevator
This is used to move an elevator from current floor to next floor for eg current floor is 1 and requested from is 5 and requested to is 7 then after hitting it one time it will move the elevator to the next floor which is requested from floor then hit it again then it will move the elevator to the requested to floor

- URL: /api/v1/elevators/{elevator_id}/move_elevator
- Method: POST
- Description: Move the elevator to the requested floors.
- Response:
```json

{
    "message": "Elevator moved successfully.",
    "elevator_id": 1,
    "current_floor": 7,
    "previous_floor": 5
}
```
