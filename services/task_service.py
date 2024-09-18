from fastapi import HTTPException, Depends
from data.config import TaskAdd, TaskUpdate
from database.init_db import AsyncSessionLocal
from database.orm_models import Task, User, Telegram, Instagram, Facebook
from sqlalchemy.future import select

from services.auth_service import get_current_user
from datetime import datetime, timezone

# Delete model from database
async def delete_soc_network(socnet_models, session):
    if socnet_models is not None:
        for model in socnet_models:
            await session.delete(model)
        await session.commit()

# Add lists of telegram models into the database
async def add_telegram_to_db(tg_list, session, task_id: int):
    if tg_list is not None:
        for i in tg_list:
            tg_db = Telegram(
                url=i.url,
                username=i.username,
                bio=i.description,
                followers=i.followers,
                verified=i.verified,
                task_id=task_id
            )
            session.add(tg_db)
        await session.commit()

# Add lists of instagram models into the database
async def add_instagram_to_db(insta_list, session, task_id: int):
    if insta_list is not None:
        for i in insta_list:
            insta_db = Instagram(
                url=i.url,
                username=i.username,
                bio=i.description,
                followers=i.followers,
                verified=i.verified,
                task_id=task_id
            )
            session.add(insta_db)
        await session.commit()

# Add lists of facebook models into the database
async def add_facebook_to_db(fb_list, session, task_id: int):
    if fb_list is not None:
        for i in fb_list:
            fb_db = Facebook(
                url=i.url,
                username=i.username,
                bio=i.description,
                followers=i.followers,
                verified=i.verified,
                task_id=task_id
            )
            session.add(fb_db)
        await session.commit()

async def GetAllTasks():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Task))
        tasks = result.scalars().all()
    return {"tasks": tasks}
async def AddNewTask(task: TaskAdd, current_user: User = Depends(get_current_user)):
    async with AsyncSessionLocal() as session:

        # Create DB model Task
        new_task = Task(
            title=task.title,
            description=task.description,
            user_id=current_user.id
        )

        session.add(new_task)
        await session.commit()

        # Add JSON models to the corresponding lists
        telegrams = [soc for soc in task.social_networks if soc.soc_network == "Telegram"]
        instagrams = [soc for soc in task.social_networks if soc.soc_network == "Instagram"]
        facebooks = [soc for soc in task.social_networks if soc.soc_network == "Facebook"]

        # Add lists to the db
        await add_telegram_to_db(telegrams, session=session, task_id=new_task.id)
        await add_instagram_to_db(instagrams, session=session, task_id=new_task.id)
        await add_facebook_to_db(facebooks, session=session, task_id=new_task.id)

        print(task)

    return {
        "message": "Task added successfully",
        "task": new_task,
        "social_networks": {"telegram": telegrams, "instagram": instagrams, "facebook": facebooks}
    }

async def GetTaskByID(task_id: int, current_user: User = Depends(get_current_user)):
    async with AsyncSessionLocal() as session:

        # Get a task by ID
        result = await session.execute(select(Task).filter_by(id=task_id, user_id=current_user.id))
        task = result.scalars().first()

        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        telegrams = await session.execute(select(Telegram).filter_by(task_id=task.id))
        instagrams = await session.execute(select(Instagram).filter_by(task_id=task.id))
        facebooks = await session.execute(select(Facebook).filter_by(task_id=task.id))

    return {'task': task, 'telegram': telegrams.scalars().all(), 'instagram': instagrams.scalars().all(), 'facebook': facebooks.scalars().all()}


async def UpdateTaskByID(task_id: int, task_update: TaskUpdate, current_user: User = Depends(get_current_user)):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Task).filter_by(id=task_id, user_id=current_user.id))
        task = result.scalars().first()

        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        task.title = task_update.title
        task.description = task_update.description
        task.updated_at = datetime.now(timezone.utc)
        task.completed = task_update.completed

        await session.commit()

    return {"message": "Task updated", "task": task}


async def DeleteTaskByID(task_id: int, current_user: User = Depends(get_current_user)):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Task).filter_by(id=task_id, user_id=current_user.id))
        task = result.scalars().first()

        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        print(task)

        telegrams = await session.execute(select(Telegram).filter_by(task_id=task.id))
        instagrams = await session.execute(select(Instagram).filter_by(task_id=task.id))
        facebooks = await session.execute(select(Facebook).filter_by(task_id=task.id))

        await delete_soc_network(telegrams.scalars().all(), session=session)
        await delete_soc_network(instagrams.scalars().all(), session=session)
        await delete_soc_network(facebooks.scalars().all(), session=session)

        await session.delete(task)
        await session.commit()

    return {"message": "Task deleted"}