from sqlalchemy.orm import Session

from app.models.menu_item import MenuItem
from app.schemas.menu_item import MenuItemCreate


def create_menu_item(db: Session, item: MenuItemCreate):
    new_item = MenuItem(
        name=item.name,
        description=item.description,
        price=item.price,
        category=item.category,
        available=item.available
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


def get_available_menu_items(
    db: Session,
    category: str | None = None,
    search: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None
):
    query = (
        db.query(MenuItem)
        .filter(MenuItem.available.is_(True))
    )

    if category:
        query = query.filter(
            MenuItem.category.ilike(category)
        )

    if search:
        query = query.filter(
            MenuItem.name.ilike(f"%{search}%")
        )
    if min_price is not None:
      query = query.filter(
        MenuItem.price >= min_price
    )

    if max_price is not None:
        query = query.filter(
            MenuItem.price <= max_price
        )

    return (
        query
        .order_by(MenuItem.category, MenuItem.name)
        .all()
    )
    query = (
        db.query(MenuItem)
        .filter(MenuItem.available.is_(True))
    )

    if category:
        query = query.filter(
    MenuItem.category.ilike(category)
)
    return (
        query
        .order_by(MenuItem.category, MenuItem.name)
        .all()
    )