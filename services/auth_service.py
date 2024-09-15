from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Header
from sqlalchemy.future import select
from data.config import SECRET_KEY, ALGORITHM
from database.orm_models import User
from database.init_db import AsyncSessionLocal
import jwt
import re

#TODO need to do one class AuthService, then initialize in app, and use in all chart of code
def check_is_email(email: str):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.fullmatch(regex, email)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(token: str = Header(...)):
    async with AsyncSessionLocal() as session:
        payload = verify_token(token)
        user_email = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")

        result = await session.execute(select(User).filter_by(email=user_email))
        db_user = result.scalars().first()

        if db_user is None:
            raise HTTPException(status_code=401, detail="User not found")

    return db_user