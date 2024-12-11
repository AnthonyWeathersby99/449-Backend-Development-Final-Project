from fastapi import FastAPI, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from . import crud, models, schemas, database, auth, utils
from .auth import get_current_user, get_current_admin

def init_db():
    database.Base.metadata.drop_all(bind=database.engine)
    database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

init_db()


@app.on_event("startup")
async def startup_event():
    db = next(database.get_session_local())
    try:
        # Create admin user if not exists
        print("Checking for admin user...")
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        if not admin:
            print("Creating admin user...")
            admin = models.User(
                username="admin",
                hashed_password="password",  # In production, use proper password hashing
                is_admin=True
            )
            db.add(admin)
            db.commit()
            print("Admin user created successfully")

        # Create default plan if not exists
        default_plan = db.query(models.Plan).filter(models.Plan.name == "Full Access Plan").first()
        if not default_plan:
            print("Creating default plan...")
            default_plan = models.Plan(
                name="Full Access Plan",
                description="Access to all cloud services",
                api_permissions="storage,compute,database,analytics,ai,messaging",
                usage_limit=1000
            )
            db.add(default_plan)
            db.commit()
            print("Default plan created successfully")

    except Exception as e:
        print(f"Error during startup: {e}")
    finally:
        db.close()


# Ensure database tables are created
database.Base.metadata.create_all(bind=database.engine)


# Subscription Plan Management

# Read all plans
@app.get("/plans/", response_model=list[schemas.Plan])
def read_plans(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_session_local)
):
    """Retrieve all subscription plans"""
    plans = crud.get_plans(db, skip=skip, limit=limit)
    return plans

# Create plan
@app.post("/plans/", response_model=schemas.Plan)
def create_plan(
    plan: schemas.PlanCreate,
    db: Session = Depends(database.get_session_local),
    current_user: models.User = Depends(get_current_admin)
):
    """Create a new subscription plan"""
    return crud.create_plan(db=db, plan=plan)


# Update plan
@app.put("/plans/{plan_id}", response_model=schemas.Plan)
def update_plan(
    plan_id: int,
    plan: schemas.PlanUpdate,
    db: Session = Depends(database.get_session_local),
    current_user: models.User = Depends(get_current_admin)
):
    """Update an existing subscription plan"""
    return crud.update_plan(db=db, plan_id=plan_id, plan=plan)


# Delete plan
@app.delete("/plans/{plan_id}", response_model=schemas.Plan)
def delete_plan(
    plan_id: int,
    db: Session = Depends(database.get_session_local),
    current_user: models.User = Depends(get_current_admin)
):
    """Delete a subscription plan"""
    return crud.delete_plan(db=db, plan_id=plan_id)

# Permission Management
@app.post("/permissions/", response_model=schemas.Permission)
def create_permission(
    permission: schemas.PermissionCreate,
    db: Session = Depends(database.get_session_local),
    current_user: models.User = Depends(get_current_admin)
):
    return crud.create_permission(db, permission)

@app.get("/permissions/", response_model=list[schemas.Permission])
def read_permissions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_session_local),
    current_user: models.User = Depends(get_current_admin)
):
    return crud.get_permissions(db, skip=skip, limit=limit)

@app.put("/permissions/{permission_id}", response_model=schemas.Permission)
def update_permission(
    permission_id: int,
    permission: schemas.PermissionUpdate,
    db: Session = Depends(database.get_session_local),
    current_user: models.User = Depends(get_current_admin)
):
    db_permission = crud.get_permission(db, permission_id=permission_id)
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return crud.update_permission(db=db, permission_id=permission_id, permission=permission)

@app.delete("/permissions/{permission_id}", response_model=schemas.Permission)
def delete_permission(
    permission_id: int,
    db: Session = Depends(database.get_session_local),
    current_user: models.User = Depends(get_current_admin)
):
    db_permission = crud.get_permission(db, permission_id=permission_id)
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return crud.delete_permission(db=db, permission_id=permission_id)

@app.post("/token")
async def login_for_access_token(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(database.get_session_local)
):
    # Print debug info
    print(f"Login attempt - username: {username}, password: {password}")

    user = db.query(models.User).filter(models.User.username == username).first()

    # Print debug info
    print(f"Found user: {user}")

    if user and user.hashed_password == password:  # In production, use proper password hashing
        return {"access_token": "admin_token", "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid username or password")

# Sample Cloud Services (Add 6 example APIs)
@app.get("/api/storage")
async def storage_service(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_session_local)
):
    utils.check_usage_limit(db, current_user, "storage")
    return {"message": "Storage service accessed"}

@app.get("/api/compute")
async def compute_service(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_session_local)
):
    utils.check_usage_limit(db, current_user, "compute")
    return {"message": "Compute service accessed"}

# User Subscription Management
@app.post("/subscriptions/{plan_id}")
async def subscribe_to_plan(
    plan_id: int,
    db: Session = Depends(database.get_session_local),
    current_user: models.User = Depends(get_current_user)
):
    plan = crud.get_plan(db, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    current_user.subscription_plan_id = plan_id
    db.commit()
    return {"message": "Successfully subscribed to plan"}


@app.get("/subscriptions/{user_id}", response_model=schemas.Plan)
async def view_subscription_details(
    user_id: int,
    db: Session = Depends(database.get_session_local),
    current_user: models.User = Depends(get_current_user)
):
    """View current subscription details"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.subscription_plan

@app.get("/subscriptions/{user_id}/usage")
async def view_usage_statistics(
    user_id: int,
    db: Session = Depends(database.get_session_local),
    current_user: models.User = Depends(get_current_user)
):
    """View usage statistics"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "total_api_calls": user.usage_count,
        "usage_limit": user.subscription_plan.usage_limit if user.subscription_plan else 0,
        "remaining_calls": (user.subscription_plan.usage_limit - user.usage_count)
            if user.subscription_plan else 0
    }

@app.put("/subscriptions/{user_id}")
async def modify_user_subscription(
    user_id: int,
    plan: schemas.SubscriptionUpdate,
    db: Session = Depends(database.get_session_local),
    current_user: models.User = Depends(get_current_admin)
):
    """Admin endpoint to modify a user's subscription"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_plan = crud.get_plan(db, plan.plan_id)
    if not new_plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    user.subscription_plan_id = plan.plan_id
    db.commit()
    return {"message": "Subscription updated successfully"}


@app.get("/access/{user_id}/{api_name}")
async def check_access_permission(
    user_id: int,
    api_name: str,
    db: Session = Depends(database.get_session_local)
):
    """Check if user has permission to access specific API"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user or not user.subscription_plan:
        return {"has_access": False, "reason": "No active subscription"}

    allowed_apis = user.subscription_plan.api_permissions.split(',')
    has_access = api_name in allowed_apis and user.usage_count < user.subscription_plan.usage_limit

    return {
        "has_access": has_access,
        "current_usage": user.usage_count,
        "limit": user.subscription_plan.usage_limit
    }

@app.post("/usage/{user_id}")
async def track_api_usage(
    user_id: int,
    usage: schemas.UsageCreate,
    db: Session = Depends(database.get_session_local)
):
    """Track API usage for a user"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.subscription_plan:
        raise HTTPException(status_code=403, detail="No active subscription")

    # Check if API is allowed in user's plan
    allowed_apis = user.subscription_plan.api_permissions.split(',')
    if usage.api_name not in allowed_apis:
        raise HTTPException(status_code=403, detail="API not included in subscription plan")

    user.usage_count += 1
    db.commit()

    return {
        "current_usage": user.usage_count,
        "api_name": usage.api_name,
        "usage_limit": user.subscription_plan.usage_limit
    }

@app.get("/api/database")
async def database_service(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_session_local)
):
    utils.check_usage_limit(db, current_user, "database")
    return {"message": "Database service accessed"}

@app.get("/api/analytics")
async def analytics_service(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_session_local)
):
    utils.check_usage_limit(db, current_user, "analytics")
    return {"message": "Analytics service accessed"}

@app.get("/api/ai")
async def ai_service(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_session_local)
):
    utils.check_usage_limit(db, current_user, "ai")
    return {"message": "AI service accessed"}

@app.get("/api/messaging")
async def messaging_service(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_session_local)
):
    utils.check_usage_limit(db, current_user, "messaging")
    return {"message": "Messaging service accessed"}

@app.get("/api/database")
async def database_service(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_session_local)
):
    utils.check_usage_limit(db, current_user, "database")
    return {"message": "Database service accessed"}

@app.get("/api/analytics")
async def analytics_service(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_session_local)
):
    utils.check_usage_limit(db, current_user, "analytics")
    return {"message": "Analytics service accessed"}

@app.get("/api/ai")
async def ai_service(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_session_local)
):
    utils.check_usage_limit(db, current_user, "ai")
    return {"message": "AI service accessed"}

@app.get("/api/messaging")
async def messaging_service(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_session_local)
):
    utils.check_usage_limit(db, current_user, "messaging")
    return {"message": "Messaging service accessed"}
