from fastapi import APIRouter

from data.config import UserAdd, UserLogin
from app.init_services import user_services

router = APIRouter()

@router.post('/login')
async def login(user: UserLogin):
    return await user_services.Authorization(user)

@router.post('/signin')
async def signin(user: UserAdd):
    return await user_services.Register(user)