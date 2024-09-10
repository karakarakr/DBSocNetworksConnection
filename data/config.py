#TODO all default fields need write into this file 
#FOR EXAMPLE

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
