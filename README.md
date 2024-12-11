# Cloud Service Access Management System
## Authors
- **Anthony Weathersby**
- **Emmanuel Montoya**
- **Renzo Salosagcol**
  
## Project Overview
This project implements a robust backend system for managing cloud service access using FastAPI. It provides comprehensive API endpoints for subscription management, usage tracking, and access control. The system allows administrators to create and manage subscription plans while enabling customers to access various cloud services based on their subscription levels.

## Features
- **User Authentication**: Secure JWT-based authentication system with admin and customer roles
- **Subscription Plan Management**: 
  - Create, update, and delete subscription plans
  - Define usage limits and API permissions per plan
- **Permission Management**: 
  - Granular control over API access permissions
  - Dynamic permission assignment to subscription plans
- **Usage Tracking**: 
  - Real-time tracking of API usage
  - Automatic enforcement of usage limits
- **Cloud Service Simulation**: 
  - Six mock cloud services (Storage, Compute, Database, Analytics, AI, Messaging)
  - Service access control based on subscription plans
- **Admin Dashboard**: Comprehensive management endpoints for administrators

## Tech Stack
- **Python 3.10+**: Core programming language
- **FastAPI**: High-performance web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **SQLite**: Database (can be easily switched to other SQL databases)
- **uvicorn**: ASGI server implementation
- **python-jose**: JWT token handling
- **passlib**: Password hashing
- **python-multipart**: Form data parsing

## Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Virtual environment

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/AnthonyWeathersby99/449-Backend-Development-Final-Project.git
   cd 449-Backend-Development-Final-Project
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate   # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
   ```

## Running the Application
1. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

2. Access the API documentation:
   - Swagger UI: http://127.0.0.1:8000/docs

## API Documentation

### Authentication

#### Login for Access Token
```http
POST http://127.0.0.1:8000/token
Content-Type: application/x-www-form-urlencoded

username=admin&password=password
```

### Plan Management

#### List All Plans
```http
GET http://127.0.0.1:8000/plans
Authorization: Bearer admin_token
```

#### Create New Plan
```http
POST http://127.0.0.1:8000/plans
Authorization: Bearer admin_token
Content-Type: application/json

{
    "name": "Basic Plan",
    "description": "Basic cloud services access",
    "api_permissions": "storage,compute",
    "usage_limit": 100
}
```

#### Update Plan
```http
PUT http://127.0.0.1:8000/plans/1
Authorization: Bearer admin_token
Content-Type: application/json

{
    "name": "Updated Basic Plan",
    "description": "Updated description",
    "api_permissions": "storage,compute,database",
    "usage_limit": 150
}
```

#### Delete Plan
```http
DELETE http://127.0.0.1:8000/plans/1
Authorization: Bearer admin_token
```

### Permission Management

#### List All Permissions
```http
GET http://127.0.0.1:8000/permissions
Authorization: Bearer admin_token
```

#### Create Permission
```http
POST http://127.0.0.1:8000/permissions
Authorization: Bearer admin_token
Content-Type: application/json

{
    "name": "storage_access",
    "description": "Access to storage API"
}
```

#### Update Permission
```http
PUT http://127.0.0.1:8000/permissions/1
Authorization: Bearer admin_token
Content-Type: application/json

{
    "name": "updated_storage_access",
    "description": "Updated storage API access"
}
```

#### Delete Permission
```http
DELETE http://127.0.0.1:8000/permissions/1
Authorization: Bearer admin_token
```

### Subscription Management

#### Subscribe to Plan
```http
POST http://127.0.0.1:8000/subscriptions/1
Authorization: Bearer admin_token
```

#### View Subscription Details
```http
GET http://127.0.0.1:8000/subscriptions/1
Authorization: Bearer admin_token
```

#### View Usage Statistics
```http
GET http://127.0.0.1:8000/subscriptions/1/usage
Authorization: Bearer admin_token
```

#### Modify User's Subscription
```http
PUT http://127.0.0.1:8000/subscriptions/1
Authorization: Bearer admin_token
Content-Type: application/json

{
    "plan_id": 2
}
```

### Access Control & Usage

#### Check Access Permission
```http
GET http://127.0.0.1:8000/access/1/storage
Authorization: Bearer admin_token
```

#### Track API Usage
```http
POST http://127.0.0.1:8000/usage/1
Authorization: Bearer admin_token
Content-Type: application/json

{
    "api_name": "storage"
}
```

### Cloud Services

All cloud service endpoints require the following header:
```http
Authorization: Bearer admin_token
```

#### Storage Service
```http
GET http://127.0.0.1:8000/api/storage
```

#### Compute Service
```http
GET http://127.0.0.1:8000/api/compute
```

#### Database Service
```http
GET http://127.0.0.1:8000/api/database
```

#### Analytics Service
```http
GET http://127.0.0.1:8000/api/analytics
```

#### AI Service
```http
GET http://127.0.0.1:8000/api/ai
```

#### Messaging Service
```http
GET http://127.0.0.1:8000/api/messaging
```
