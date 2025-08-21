# backend/models.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional

class Merchant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Claim(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: str = Field(index=True)
    customer_email: str = Field(index=True)
    reason: str
    details: str = ""
    status: str = Field(default="new", index=True)  # new|in_review|approved|rejected
    created_at: datetime = Field(default_factory=datetime.utcnow)
    merchant_id: Optional[int] = Field(default=None, foreign_key="merchant.id")
