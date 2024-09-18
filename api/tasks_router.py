from fastapi import APIRouter, Depends

from services.auth_service import get_current_user
from services.task_service import (
    GetAllTasks,
    AddNewTask,
    GetTaskByID,
    UpdateTaskByID,
    DeleteTaskByID
)

from data.config import TaskAdd, TaskUpdate
from database.orm_models import User

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get('/tasks', dependencies=[Depends(get_current_user)])
async def get_all_tasks():
    return await GetAllTasks()

@router.post('/tasks', dependencies=[Depends(get_current_user)])
async def add_new_task(task: TaskAdd, current_user: User = Depends(get_current_user)):
    return await AddNewTask(task, current_user)

@router.get('/tasks/{task_id}', dependencies=[Depends(get_current_user)])
async def get_task_by_id(task_id: int, current_user: User = Depends(get_current_user)):
    return await GetTaskByID(task_id, current_user)

@router.put('/tasks/{task_id}', dependencies=[Depends(get_current_user)])
async def update_task_by_id(task_id: int, task_update: TaskUpdate, current_user: User = Depends(get_current_user)):
    return await UpdateTaskByID(task_id, task_update, current_user)

@router.delete('/tasks/{task_id}', dependencies=[Depends(get_current_user)])
async def delete_task_by_id(task_id: int, current_user: User = Depends(get_current_user)):
    return await DeleteTaskByID(task_id, current_user)