from fastapi import APIRouter

from data.config import UserAdd, UserLogin
from services.user_service import Register, Authorization

router = APIRouter()

@router.post('/login')
async def login(user: UserLogin):
    return await Authorization(user)

@router.post('/signin')
async def signin(user: UserAdd):
    return await Register(user)