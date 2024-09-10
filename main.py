from fastapi import FastAPI, HTTPException, Depends, Header
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from models.Models import TaskAdd, UserAdd, UserLogin, TaskUpdate
from models.DBModels import User, Task, Base, Telegram, Instagram, Facebook
from datetime import datetime, timedelta, timezone
import bcrypt
import re
import secrets
import jwt

# Initialize object "app" of class FastAPI
app = FastAPI()

# Create key for authorization
# And what kind of hash algorithm
SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"

# Create async engine to connect to postgresql db
engine = create_async_engine(
    'postgresql+asyncpg://postgres:123@localhost/postgres',
    echo=True
)

# Create AsyncSession
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Create all tables in the database
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Create token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

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

# Check was token expired or is it invalid
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def CheckIsEmail(email: str):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.fullmatch(regex, email)

# Dependency to check for Authorization token
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

# Login into your existing account
@app.post('/login')
async def Authorization(user: UserLogin):
    async with AsyncSessionLocal() as session:

        # Hash password using bcrypt library to compare user passwords
        byte_pswd = str.encode(user.password)
        result = await session.execute(select(User).filter_by(email=user.email))
        db_user = result.scalars().first()

        if db_user is None or not bcrypt.checkpw(byte_pswd, db_user.password.encode('utf-8')):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Create a new account
@app.post('/signin')
async def Register(user: UserAdd):
    async with AsyncSessionLocal() as session:
        if CheckIsEmail(user.email) is None:
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


@app.get('/tasks', dependencies=[Depends(get_current_user)])
async def GetAllTasks():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Task))
        tasks = result.scalars().all()
    return {"tasks": tasks}

# Add new task to db using POST method
@app.post('/tasks', dependencies=[Depends(get_current_user)])
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

@app.get('/tasks/{task_id}', dependencies=[Depends(get_current_user)])
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


@app.put('/tasks/{task_id}', dependencies=[Depends(get_current_user)])
async def UpdateTaskByID(task_id: int, task_update: TaskUpdate, current_user: User = Depends(get_current_user)):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Task).filter_by(id=task_id, user_id=current_user.id))
        task = result.scalars().first()

        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        task.title = task_update.title
        task.description = task_update.description
        task.updated_at = datetime.now(timezone.utc)

        await session.commit()

    return {"message": "Task updated", "task": task}


@app.delete('/tasks/{task_id}', dependencies=[Depends(get_current_user)])
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

