from pydantic import BaseModel
from decimal import Decimal

class LeadBase(BaseModel):
    name: str
    location: str
    budget: Decimal

class LeadCreate(LeadBase):
    pass

class Lead(LeadBase):
    id: int

    class Config:
        orm_mode = True
