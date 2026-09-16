from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserCreate
from app.auth.security import hash_password, verify_password, create_access_token


def create_user(db: Session, user: UserCreate):
    existing_user = db.scalar(
        select(User).where(User.email == user.email)
    )

    if existing_user:
        raise ValueError("Email already exists")

    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(db: Session, email: str, password: str):
    user = db.scalar(
        select(User).where(User.email == email)
    )

    if not user:
        raise ValueError("Invalid email or password")

    if not user.password_hash:
        raise ValueError("Invalid email or password")

    if not verify_password(password, user.password_hash):
        raise ValueError("Invalid email or password")

    return create_access_token(user.id, user.role)