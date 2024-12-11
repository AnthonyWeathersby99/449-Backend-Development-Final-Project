from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas

def create_plan(db: Session, plan: schemas.PlanCreate):
    db_plan = models.Plan(**plan.dict())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

def update_plan(db: Session, plan_id: int, plan: schemas.PlanUpdate):
    db_plan = db.query(models.Plan).filter(models.Plan.id == plan_id).first()
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    for key, value in plan.dict(exclude_unset=True).items():
        setattr(db_plan, key, value)
    db.commit()
    db.refresh(db_plan)
    return db_plan

def delete_plan(db: Session, plan_id: int):
    db_plan = db.query(models.Plan).filter(models.Plan.id == plan_id).first()
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    db.delete(db_plan)
    db.commit()
    return {"detail": "Plan deleted"}

def create_permission(db: Session, permission: schemas.PermissionCreate):
    db_permission = models.Permission(**permission.dict())
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

def get_permissions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Permission).offset(skip).limit(limit).all()

def get_permission(db: Session, permission_id: int):
    return db.query(models.Permission).filter(models.Permission.id == permission_id).first()

def update_permission(db: Session, permission_id: int, permission: schemas.PermissionUpdate):
    db_permission = db.query(models.Permission).filter(models.Permission.id == permission_id).first()
    if db_permission:
        for key, value in permission.dict(exclude_unset=True).items():
            setattr(db_permission, key, value)
        db.commit()
        db.refresh(db_permission)
    return db_permission

def delete_permission(db: Session, permission_id: int):
    db_permission = db.query(models.Permission).filter(models.Permission.id == permission_id).first()
    if db_permission:
        db.delete(db_permission)
        db.commit()
    return db_permission
