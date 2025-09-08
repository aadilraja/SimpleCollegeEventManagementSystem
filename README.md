# College Event Management System

This project is a simple RESTful API built with Python Flask and SQLAlchemy for event management. It enables efficient event management and provides students with easy access to and updates about the events.

## Features
- **User Management**: Users can create, log in, and log out of their accounts. Users also have two distinct roles: "USER" and "ADMIN".

- **JWT Based Authentication**: When a user logs in, it generates a JWT token which carries metadata about the user, such as the user role. So, the server does not have to keep looking at the database to check the user's role. it can extract it from the token, which reduces load and increases speed.

- **Http Only Cookie**: the recieved jwt token is stored as http only cookie which is very secure as client( javascript) can't edit it.

- **Role-Based Access**: Users need to have the required role or authority to access certain endpoints.

- **College & Event Management**: Admins are able to add, delete, and view events and the students who applied to them. They can also mark student attendance.


# Getting Started
Follow these instructions to configure the project and run it.

## Prerequisites
- Python 3.10+
- **pip** (Python package installer)

### On Windows (PowerShell):
```PowerShell
# Create the virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\Activate
```
### On macOS / Linux:
```Bash
# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### Install dependencies

```Bash
pip install -r requirements.txt
```

### Run the Application
```Bash
python app.py
```



# Working

The project is divided into 3 layers following the principle of the Model-View-Controller (MVC) pattern.

This makes the API easier to understand and maintain, which helps in scaling the application.

## Model-Layer
The Model layer are representation of the database entities directly. It maps application objects to database tables.

In my project, these models are located under src/Entity and they are:-

- Colleges: represent User college or college who is hosting the event
- Event: represent Event that are been hosted such as tech talk, hackathon
- Registeration: represent the user who registered for a specific event
User: Represents a user who has an account in the system.

## View-Layer
This layer is representation of data that is been send to the Client. In this project we are sending json data

this layer is located in src/Serializer

## Controller-Layer

The Controller is the layer of Server api that directly interact with client, it recieves Request from client and based on that it gives Response

This project is Restful api so it recieves http request, which are CRUD operation.

It send response in json after CRUD operation.

## The Service Layer (Business Logic)

It sits between Controller and Model and perform business logic like "find or create" logic for a college, checking if a User is already registered for an event
eg, if User entered college name doesnt exist create a college with following name



## API Endpoints:-
- POST /users: Create a new user.

- POST /users/login: Log in and receive jwt token as Http only cookies.

- POST /users/logout: Log out and clear the Http Only cookies.

- GET /events: (User/Admin) Browse all events.

- POST /events/{event_id}/register: (User) Register for an event.

- POST /events: (Admin) Create a new event.

- PUT /events/{event_id}: (Admin) Update an event.

- DELETE /events/{event_id}: (Admin) Delete an event.

- GET /events/dashboard: (Admin) View all events with registered students

- POST /registrations/{reg_id}/check-in: (Admin) Mark a student as attended.
