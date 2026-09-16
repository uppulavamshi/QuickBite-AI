from app.auth.security import get_current_user_id, require_staff
from app.database.base import Base
from app.database.connection import engine
from app.models.user import User
from app.models.menu_item import MenuItem
from app.models.order import Order
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin
from app.services.user_service import create_user, login_user
from app.schemas.menu_item import MenuItemCreate, MenuItemResponse
from app.services.menu_item_service import (
    create_menu_item,
    get_available_menu_items,
)
from app.services.menu_item_service import (
    create_menu_item,
    get_available_menu_items
)
from app.schemas.order import (
    OrderCreate,
    StudentOrderCreate,
    OrderResponse,
    OrderDetailResponse,
    OrderStatusUpdate,
)
from app.services.order_service import (
    create_order,
    get_orders,
    get_order,
    get_user_orders,
    update_order_status,
)
Base.metadata.create_all(bind=engine)

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

app = FastAPI(
    title="QuickBite AI API",
    version="1.0.0"
)

@app.get("/me")
def get_me(
    user_id: int = Depends(get_current_user_id)
):
    return {
        "user_id": user_id
    }

@app.post(
    "/users",
    responses={
        409: {"description": "Email already exists"}
    }
)
def create_user_endpoint(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_user(db, user)
    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )

@app.post("/login")
def login_endpoint(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    try:
        token = login_user(db, user.email, user.password)
        return {
            "access_token": token,
            "token_type": "bearer"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )

@app.post("/menu-items", response_model=MenuItemResponse)
def create_menu_item_endpoint(
    item: MenuItemCreate,
    db: Session = Depends(get_db)
):
    return create_menu_item(db, item)
@app.get("/menu-items", response_model=list[MenuItemResponse])
def get_menu_items(
    category: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db)
):
    return get_available_menu_items(
        db,
        category,
        search
    )
@app.get(
    "/menu-items/available",
    response_model=list[MenuItemResponse]
)
def get_available_menu_items_endpoint(
    category: str | None = None,
    search: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    db: Session = Depends(get_db)
):
    return get_available_menu_items(
    db,
    category,
    search,
    min_price,
    max_price
)

@app.post(
    "/orders",
    response_model=OrderResponse,
    responses={
        400: {"description": "User or menu item validation failed"}
    }
)
def create_order_endpoint(
    order: OrderCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    try:
      return create_order(db, order, user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@app.get("/orders", response_model=list[OrderDetailResponse])
def get_orders_endpoint(
    staff = Depends(require_staff),
    db: Session = Depends(get_db)
):
    return get_orders(db)
@app.get(
    "/orders/{order_id}",
    response_model=OrderDetailResponse,
    responses={
        404: {"description": "Order not found"},
    },
)
def get_order_endpoint(
    order_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    try:
        return get_order(db, order_id, user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
@app.get(
    "/users/{user_id}/orders",
    response_model=list[OrderDetailResponse],
    responses={
        404: {"description": "User not found"},
    },
)
def get_user_orders_endpoint(
    user_id: int,
    staff = Depends(require_staff),
    db: Session = Depends(get_db)
):
    try:
        return get_user_orders(db, user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
@app.get(
    "/me/orders",
    response_model=list[OrderDetailResponse],
)
def get_my_orders_endpoint(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    try:
        return get_user_orders(db, user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@app.patch(
    "/orders/{order_id}/status",
    response_model=OrderResponse,
    responses={
        400: {"description": "Invalid status transition"},
        404: {"description": "Order not found"},
    },
)
def update_order_status_endpoint(
    order_id: int,
    status_update: OrderStatusUpdate,
    staff = Depends(require_staff),
    db: Session = Depends(get_db)
):
    try:
        return update_order_status(
            db,
            order_id,
            status_update.status
        )
    except ValueError as e:
        if str(e) == "Order not found":
            raise HTTPException(
                status_code=404,
                detail=str(e)
            )

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )