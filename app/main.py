from fastapi import FastAPI, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from . import crud, models, schemas, database, auth, utils
from .auth import get_current_admin

app = FastAPI()

# Ensure database tables are created
database.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Cloud Service Access Management System API!"}

# Subscription Plan Management
@app.post("/plans/", response_model=schemas.Plan)
def create_plan(
    plan: schemas.PlanCreate,
    db: Session = Depends(database.get_session_local),
    current_user: models.User = Depends(get_current_admin)
):
    return crud.create_plan(db=db, plan=plan)

@app.put("/plans/{plan_id}", response_model=schemas.Plan)
def update_plan(
    plan_id: int,
    plan: schemas.PlanUpdate,
    db: Session = Depends(database.get_session_local),
    current_user: models.User = Depends(get_current_admin)
):
    db_plan = crud.get_plan(db, plan_id=plan_id)
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return crud.update_plan(db=db, plan_id=plan_id, plan=plan)

@app.delete("/plans/{plan_id}", response_model=schemas.Plan)
def delete_plan(
    plan_id: int,
    db: Session = Depends(database.get_session_local),
    current_user: models.User = Depends(get_current_admin)
):
    db_plan = crud.get_plan(db, plan_id=plan_id)
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
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

@app.post("/token", response_model=dict)
def login_for_access_token(
    username: str = Form(...),  # Use Form to accept form data
    password: str = Form(...),  # Use Form to accept form data
    db: Session = Depends(database.get_session_local)
):
    # Simulated token generation
    if username == "admin" and password == "password":
        return {"access_token": "admin_token", "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid username or password")
