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
- **POST** `/token`: Obtain access token
  ```bash
  curl -X POST "http://localhost:8000/token" -d "username=admin&password=password"
  ```

### Subscription Plans
- **GET** `/plans/`: List all subscription plans
- **POST** `/plans/`: Create new plan (Admin only)
- **PUT** `/plans/{plan_id}`: Update plan (Admin only)
- **DELETE** `/plans/{plan_id}`: Delete plan (Admin only)

### User Subscriptions
- **POST** `/subscriptions/{plan_id}`: Subscribe to a plan
- **GET** `/subscriptions/{user_id}`: View subscription details
- **GET** `/subscriptions/{user_id}/usage`: Check usage statistics

### Cloud Services
- **GET** `/api/storage`: Access storage service
- **GET** `/api/compute`: Access compute service
- **GET** `/api/database`: Access database service
- **GET** `/api/analytics`: Access analytics service
- **GET** `/api/ai`: Access AI service
- **GET** `/api/messaging`: Access messaging service
