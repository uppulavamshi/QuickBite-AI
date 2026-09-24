from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.user import User
from app.models.menu_item import MenuItem
from app.schemas.order import OrderCreate, OrderStatus


def build_order_detail(order: Order):
    return {
        "id": order.id,
        "user_id": order.user_id,
        "user_name": order.user.name,
        "menu_item_id": order.menu_item_id,
        "menu_item_name": order.menu_item.name,
        "quantity": order.quantity,
        "status": OrderStatus(order.status),
        "created_at": order.created_at,
    }


def create_order(db: Session, order: OrderCreate, user_id: int):
    user = db.get(User, user_id)

    if not user:
        raise ValueError("User not found")

    menu_item = db.get(MenuItem, order.menu_item_id)

    if not menu_item:
        raise ValueError("Menu item not found")

    if not menu_item.available:
        raise ValueError("Menu item is not available")

    new_order = Order(
        user_id=user_id,
        menu_item_id=order.menu_item_id,
        quantity=order.quantity
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


def get_orders(
    db: Session,
    page: int,
    limit: int
):
    offset = (page - 1) * limit

    orders = (
        db.query(Order)
        .order_by(Order.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return [
        build_order_detail(order)
        for order in orders
    ]


def update_order_status(
    db: Session,
    order_id: int,
    status: OrderStatus
):
    order = db.get(Order, order_id)

    if not order:
        raise ValueError("Order not found")

    current_status = OrderStatus(order.status)

    allowed_transitions = {
        OrderStatus.pending: OrderStatus.preparing,
        OrderStatus.preparing: OrderStatus.ready,
        OrderStatus.ready: OrderStatus.collected,
    }

    expected_next_status = allowed_transitions.get(current_status)

    if status != expected_next_status:
        raise ValueError(
            f"Invalid status transition: "
            f"{current_status.value} → {status.value}"
        )

    order.status = status.value

    db.commit()
    db.refresh(order)

    return order


def get_order(db: Session, order_id: int, user_id: int):
    order = db.get(Order, order_id)

    if not order:
        raise ValueError("Order not found")

    if order.user_id != user_id:
        raise ValueError("Order not found")

    return build_order_detail(order)


def get_user_orders(db: Session, user_id: int):
    user = db.get(User, user_id)

    if not user:
        raise ValueError("User not found")

    orders = (
        db.query(Order)
        .filter(Order.user_id == user_id)
        .order_by(Order.id.desc())
        .all()
    )

    return [
        build_order_detail(order)
        for order in orders
    ]