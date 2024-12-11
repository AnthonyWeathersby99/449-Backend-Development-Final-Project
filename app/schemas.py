from pydantic import BaseModel

class PlanBase(BaseModel):
    name: str
    description: str
    api_permissions: str
    usage_limit: int

class PlanCreate(PlanBase):
    pass

class PlanUpdate(PlanBase):
    pass

class Plan(PlanBase):
    id: int

    class Config:
        from_attributes = True
