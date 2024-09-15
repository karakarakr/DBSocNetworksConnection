from fastapi import FastAPI, Depends
from services.auth_service import get_current_user
from services.task_service import (
    GetAllTasks,
    AddNewTask,
    GetTaskByID,
    UpdateTaskByID,
    DeleteTaskByID
)
from services.user_service import Register, Authorization
from database.init_db import init_db
from data.config import UserAdd, UserLogin, TaskAdd, TaskUpdate
from database.orm_models import User

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get('/')
async def start_response():
    return {"status_code" : 200}

@app.post('/login')
async def login(user: UserLogin):
    return await Authorization(user)

@app.post('/signin')
async def signin(user: UserAdd):
    return await Register(user)

@app.get('/tasks', dependencies=[Depends(get_current_user)])
async def get_all_tasks():
    return await GetAllTasks()

@app.post('/tasks', dependencies=[Depends(get_current_user)])
async def add_new_task(task: TaskAdd, current_user: User = Depends(get_current_user)):
    return await AddNewTask(task, current_user)

@app.get('/tasks/{task_id}', dependencies=[Depends(get_current_user)])
async def get_task_by_id(task_id: int, current_user: User = Depends(get_current_user)):
    return await GetTaskByID(task_id, current_user)

@app.put('/tasks/{task_id}', dependencies=[Depends(get_current_user)])
async def update_task_by_id(task_id: int, task_update: TaskUpdate, current_user: User = Depends(get_current_user)):
    return await UpdateTaskByID(task_id, task_update, current_user)

@app.delete('/tasks/{task_id}', dependencies=[Depends(get_current_user)])
async def delete_task_by_id(task_id: int, current_user: User = Depends(get_current_user)):
    return await DeleteTaskByID(task_id, current_user)