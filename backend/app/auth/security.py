import os
from fastapi import Depends, HTTPException
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
security = HTTPBearer()


def create_access_token(user_id: int, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
    "sub": str(user_id),
    "role": role,
    "exp": expire
}
    

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_access_token(token: str) -> dict:
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    return payload
def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    try:
        payload = decode_access_token(credentials.credentials)
        return int(payload["sub"])
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
def require_staff(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        payload = decode_access_token(credentials.credentials)

        if payload.get("role") != "staff":
            raise HTTPException(
                status_code=403,
                detail="Staff access required"
            )

        return payload

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )