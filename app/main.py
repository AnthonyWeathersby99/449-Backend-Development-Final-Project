from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas, database, auth, utils  # Changed to relative import

app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)

# Dependency for getting a database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Subscription Plan Management
@app.post("/plans/", response_model=schemas.Plan)
def create_plan(
    plan: schemas.PlanCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin)
):
    print(f"Request Data: {plan}")
    print(f"Current User: {current_user.username}")
    return crud.create_plan(db=db, plan=plan)

@app.put("/plans/{plan_id}", response_model=schemas.Plan)
def update_plan(plan_id: int, plan: schemas.PlanUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_admin)):
    return crud.update_plan(db=db, plan_id=plan_id, plan=plan)

@app.delete("/plans/{plan_id}")
def delete_plan(plan_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_admin)):
    return crud.delete_plan(db=db, plan_id=plan_id)
