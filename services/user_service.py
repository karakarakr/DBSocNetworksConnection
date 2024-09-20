from fastapi import HTTPException
from data.config import UserAdd, UserLogin
from database.init_db import AsyncSessionLocal
from database.orm_models import User
from sqlalchemy.future import select

from services.auth_service import auth_services

import bcrypt

#TODO need to do one class UserServices, then initialize in app, and use in all chart of code
class UserServices:

    async def Register(self, user: UserAdd):
        async with AsyncSessionLocal() as session:
            if auth_services.check_is_email(user.email) is None:
                raise HTTPException(status_code=400, detail=f'{user.email} is not a valid email!')

            hashed_password = bcrypt.hashpw(
                str.encode(user.password),
                bcrypt.gensalt()
            ).decode('utf-8')

            # Create DB model
            db_user = User(
                username=user.username,
                email=user.email,
                password=hashed_password
            )

            # Write DB model into the database
            session.add(db_user)
            await session.commit()

        return {'message': 'User was added successfully!', 'user': user}

    async def Authorization(self, user: UserLogin):
        async with AsyncSessionLocal() as session:

            # Hash password using bcrypt library to compare user passwords
            byte_pswd = str.encode(user.password)
            result = await session.execute(select(User).filter_by(email=user.email))
            db_user = result.scalars().first()

            if db_user is None or not bcrypt.checkpw(byte_pswd, db_user.password.encode('utf-8')):
                raise HTTPException(status_code=401, detail="Invalid email or password")

            access_token = auth_services.create_access_token(data={"sub": db_user.email})

        return {"access_token": access_token, "token_type": "bearer"}