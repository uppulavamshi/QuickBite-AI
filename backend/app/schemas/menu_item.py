from pydantic import BaseModel


class MenuItemCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str
    available: bool = True


class MenuItemResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: str
    available: bool

    class Config:
        from_attributes = True