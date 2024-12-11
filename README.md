# 449-Backend-Development-Final-Project
## Author
- **Anthony Weathersby**
- **Emmanuel Montoya**
- **Renzo Salosagcol**
  
## Project Overview
This project is a backend system for managing cloud service access. It allows administrators to create subscription plans, assign permissions, and track usage. The system is built using FastAPI and provides a robust API for managing users, plans, and permissions.

## Features
- **Subscription Plan Management**: Create, update, and delete subscription plans.
- **User Management**: Authenticate users and manage their roles (e.g., admin, customer).
- **Permission Management**: Define and manage API permissions for various subscription plans.
- **Usage Tracking**: Track usage based on subscription limits.

## Tech Stack
- **Python**: Core programming language.
- **FastAPI**: Framework for building the backend API.
- **SQLAlchemy**: ORM for database operations.
- **SQLite**: Default database for local development (can be swapped for PostgreSQL).
- **Pydantic**: Data validation and settings management.

## Installation

### Prerequisites
- Python 3.10 or higher
- Virtual environment setup

### Steps
1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/your-repository.git](https://github.com/AnthonyWeathersby99/449-Backend-Development-Final-Project.git)
   cd 449-Backend-Development-Final-Project
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate    # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the database (SQLite by default):
   ```bash
   python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
   ```
5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## Usage

### Access the API
Once the server is running, the API can be accessed at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Endpoints
Here are some key endpoints available:

#### Create a Subscription Plan
- **POST** `/plans/`
- **Request Body**:
  ```json
  {
    "name": "Basic Plan",
    "description": "Basic subscription plan",
    "api_permissions": "service1",
    "usage_limit": 100
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Basic Plan",
    "description": "Basic subscription plan",
    "api_permissions": "service1",
    "usage_limit": 100
  }
  ```

#### Update a Subscription Plan
- **PUT** `/plans/{plan_id}`
- **Request Body**:
  ```json
  {
    "name": "Updated Plan",
    "description": "Updated subscription plan",
    "api_permissions": "service1,service2",
    "usage_limit": 150
  }
  ```

#### Delete a Subscription Plan
- **DELETE** `/plans/{plan_id}`

#### Authentication
Include the following header for admin access:
```
Authorization: Bearer admin_token
```

## Author
- **Anthony Weathersby**
