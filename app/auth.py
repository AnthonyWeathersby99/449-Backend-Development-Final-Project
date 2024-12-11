from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models, database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_session_local)):
    if not token:
        raise HTTPException(status_code=401, detail="Authentication required")

    # For debugging
    print(f"Received token: {token}")

    # Change this to match the token format from your login endpoint
    user = db.query(models.User).filter(models.User.username == "admin").first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_session_local)):
    user = get_current_user(token, db)
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user
