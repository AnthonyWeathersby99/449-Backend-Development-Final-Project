Cloud Service Access Management System

Project Overview

The Cloud Service Access Management System manages access to cloud services based on subscription plans. This backend provides functionalities for customers and admins to manage plans, permissions, and track usage.

Prerequisites

Python 3.8+

Virtual environment tool (optional but recommended)

Installation Instructions

Clone the repository:

git clone <repository-url>
cd cloud_service_management

Set up a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'

Install the dependencies:

pip install -r requirements.txt

Run the server:

uvicorn app.main:app --reload

This will start the FastAPI server, which can be accessed at http://127.0.0.1:8000.

API Endpoints Overview

Subscription Plan Management:

POST /plans: Create a new subscription plan.

PUT /plans/{planId}: Modify an existing plan.

DELETE /plans/{planId}: Delete a plan.

Permission Management:

POST /permissions: Add a new permission.

PUT /permissions/{permissionId}: Modify an existing permission.

DELETE /permissions/{permissionId}: Delete a permission.

User Subscription Handling:

POST /subscriptions: Subscribe a user to a plan.

GET /subscriptions/{userId}: View the current subscription.

GET /subscriptions/{userId}/usage: View usage statistics.

PUT /subscriptions/{userId}: Assign or modify a user plan.

Access Control:

GET /access/{userId}/{apiRequest}: Check if a user can access a particular API.

Usage Tracking and Limit Enforcement:

POST /usage/{userId}: Track an API request by a user.

GET /usage/{userId}/limit: Check if a user has reached their subscription limit.

Testing the API

You can use Postman to interact with the API endpoints.

Import the endpoint URLs and test all features, including subscription management, permission changes, and access control.

Ensure proper authorization headers are provided for endpoints requiring admin roles.

Running Tests

Execute the test suite using pytest:

pytest tests/

This will run all test cases and report on any failures.
