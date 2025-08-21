# backend/schemas.py
from pydantic import BaseModel, EmailStr

class ClaimCreate(BaseModel):
    order_id: str
    customer_email: EmailStr
    reason: str
    details: str = ""

class ClaimOut(BaseModel):
    id: int
    order_id: str
    customer_email: EmailStr
    reason: str
    details: str
    status: str
