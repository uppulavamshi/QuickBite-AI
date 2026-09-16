from decimal import Decimal

from sqlalchemy import Boolean, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    category: Mapped[str] = mapped_column(String(50))
    available: Mapped[bool] = mapped_column(Boolean, default=True)