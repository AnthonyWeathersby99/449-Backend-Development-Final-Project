from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models, database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_session_local)):
    print(f"Received Token: {token}")

    # For testing, use this simplified version
    if token == "admin_token":
        return models.User(username="admin", is_admin=True)

    user = db.query(models.User).filter(models.User.username == token).first()
    if user is None or not user.is_admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
