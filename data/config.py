# TODO all default fields need write into this file
# FOR EXAMPLE

# import enum
# from typing import Optional
# from urllib.parse import urlparse

# from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn


# class Environment(str, enum.Enum):
#     LOCAL = "local"
#     PRODUCTION = "production"


# class Config(BaseSettings):
#     db_url: PostgresDsn
#     db_pool_min_size: Optional[int] = 5
#     db_pool_max_size: Optional[int] = 20

#     api_id: str
#     api_hash: str
#     phone_number: str
#     session_file: str

#     hunter_api: str

#     admin_mail: str

#     bot_token: str

#     host: str
#     port: str

#     notification_chat_id: int
#     admin_chat_id: str

#     sentry_dsn: Optional[str] = None
#     environment: Optional[str] = "local"

#     @property
#     def webhook_path(self) -> Optional[str]:
#         if not self.webhook_url:
#             return None
#         webhook_url = self.webhook_url
#         if not webhook_url.startswith("http"):
#             webhook_url = "https://" + webhook_url
#         return urlparse(webhook_url).path

#     class Config:
#         env_file = ".env"
#         env_file_encoding = "utf-8"

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from typing import List, Union

# Importing libs for working with enviroment files
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

class TelegramModel(BaseModel):
    soc_network: str = 'Telegram'
    url: str
    username: str
    description: Optional[str] = None
    followers: Optional[int] = None
    verified: Optional[bool] = False

class InstagramModel(BaseModel):
    soc_network: str = 'Instagram'
    url: str
    username: str
    description: Optional[str] = None
    followers: Optional[int] = None
    verified: Optional[bool] = False

class FacebookModel(BaseModel):
    soc_network: str = 'Facebook'
    url: str
    username: str
    description: Optional[str] = None
    followers: Optional[int] = None
    verified: Optional[bool] = False

class TaskAdd(BaseModel):
    #id: int = 1
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    social_networks: List[Union[
        FacebookModel, TelegramModel, InstagramModel
    ]]
    #user_id: int

class TaskUpdate(BaseModel):
    #id: int = 1
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    #user_id: int

class TaskGet(BaseModel):
    title: str
    description: str = None
    completed: bool = False
    created_at: datetime
    updated_at: datetime
    user_id: int

class UserAdd(BaseModel):
    #id: int = 1
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str
