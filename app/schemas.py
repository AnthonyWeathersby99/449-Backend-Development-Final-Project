from pydantic import BaseModel
from typing import Optional

class PlanBase(BaseModel):
    name: str
    description: str
    api_permissions: str
    usage_limit: int

class PlanCreate(PlanBase):
    pass


class PlanUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    api_permissions: Optional[str] = None
    usage_limit: Optional[int] = None

class Plan(PlanBase):
    id: int

    class Config:
        from_attributes = True

class PermissionBase(BaseModel):
    name: str
    description: str | None = None

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(PermissionBase):
    pass

class Permission(PermissionBase):
    id: int

    class Config:
        from_attributes = True
