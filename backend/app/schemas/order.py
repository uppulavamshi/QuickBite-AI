from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    pending = "pending"
    preparing = "preparing"
    ready = "ready"
    collected = "collected"


class OrderCreate(BaseModel):
    menu_item_id: int
    quantity: int = Field(default=1, ge=1)
class StudentOrderCreate(BaseModel):
    menu_item_id: int
    quantity: int = Field(default=1, ge=1)


class OrderResponse(BaseModel):
    id: int
    user_id: int
    menu_item_id: int
    quantity: int
    status: OrderStatus
    created_at: datetime

    class Config:
        from_attributes = True


class OrderDetailResponse(BaseModel):
    id: int
    user_id: int
    user_name: str
    menu_item_id: int
    menu_item_name: str
    quantity: int
    status: OrderStatus
    created_at: datetime


class OrderStatusUpdate(BaseModel):
    status: OrderStatus