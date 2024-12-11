from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models

def check_usage_limit(db: Session, user: models.User, api_name: str):
    if not user.subscription_plan:
        raise HTTPException(status_code=403, detail="No active subscription")

    if user.usage_count >= user.subscription_plan.usage_limit:
        raise HTTPException(status_code=403, detail="Usage limit reached")

    # Check if the API is allowed in the user's plan
    allowed_apis = user.subscription_plan.api_permissions.split(',')
    if api_name not in allowed_apis:
        raise HTTPException(status_code=403, detail="API not included in subscription plan")

    # Increment usage count
    user.usage_count += 1
    db.commit()
