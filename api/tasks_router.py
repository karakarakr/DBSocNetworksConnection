from fastapi import APIRouter, Depends

from services.auth_service import auth_services
from app.init_services import task_services

from data.config import TaskAdd, TaskUpdate
from database.orm_models import User

router = APIRouter(dependencies=[Depends(auth_services.get_current_user)])

@router.get('/tasks', dependencies=[Depends(auth_services.get_current_user)])
async def get_all_tasks():
    return await task_services.GetAllTasks()

@router.post('/tasks', dependencies=[Depends(auth_services.get_current_user)])
async def add_new_task(task: TaskAdd, current_user: User = Depends(auth_services.get_current_user)):
    return await task_services.AddNewTask(task, current_user)

@router.get('/tasks/{task_id}', dependencies=[Depends(auth_services.get_current_user)])
async def get_task_by_id(task_id: int, current_user: User = Depends(auth_services.get_current_user)):
    return await task_services.GetTaskByID(task_id, current_user)

@router.put('/tasks/{task_id}', dependencies=[Depends(auth_services.get_current_user)])
async def update_task_by_id(task_id: int, task_update: TaskUpdate, current_user: User = Depends(auth_services.get_current_user)):
    return await task_services.UpdateTaskByID(task_id, task_update, current_user)

@router.delete('/tasks/{task_id}', dependencies=[Depends(auth_services.get_current_user)])
async def delete_task_by_id(task_id: int, current_user: User = Depends(auth_services.get_current_user)):
    return await task_services.DeleteTaskByID(task_id, current_user)