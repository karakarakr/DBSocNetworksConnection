from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, declarative_base, relationship
from datetime import datetime, timezone

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String(60), nullable=False)
    email = mapped_column(String(60), nullable=False)
    password = mapped_column(String, nullable=False)

    tasks = relationship('Task', back_populates='user')

    def __repr__(self):
        return f'User(id={self.id}, username={self.username}, email={self.email}, password={self.password})'


class Task(Base):
    __tablename__ = 'tasks'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    title = mapped_column(String(100), nullable=False)
    description = mapped_column(String(1000))
    completed = mapped_column(Boolean, default=False)

    created_at = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc)
    )

    updated_at = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
    )

    user_id = mapped_column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='tasks')

    # tg_id = mapped_column(Integer, ForeignKey('telegram.id'))
    # instagram_id = mapped_column(Integer, ForeignKey('instagram.id'))
    # facebook_id = mapped_column(Integer, ForeignKey('facebook.id'))

    tg = relationship('Telegram', back_populates='tasks')
    instagram = relationship('Instagram', back_populates='tasks')
    facebook = relationship('Facebook', back_populates='tasks')

    def __repr__(self):
        return f'Task(id={self.id}, title={self.title}, description={self.description}, completed={self.completed}, created_at={self.created_at}, updated_at={self.updated_at}, user_id={self.user_id})'


class Telegram(Base):
    __tablename__ = 'telegram'

    id = mapped_column(Integer, autoincrement=True, primary_key=True)
    url = mapped_column(String, nullable=False)
    username = mapped_column(String, nullable=False)
    bio = mapped_column(String)
    followers = mapped_column(Integer)
    verified = mapped_column(Boolean, default=False)

    task_id = mapped_column(Integer, ForeignKey('tasks.id'))
    tasks = relationship('Task', back_populates='tg')


class Instagram(Base):
    __tablename__ = 'instagram'

    id = mapped_column(Integer, autoincrement=True, primary_key=True)
    url = mapped_column(String, nullable=False)
    username = mapped_column(String, nullable=False)
    bio = mapped_column(String)
    followers = mapped_column(Integer)
    verified = mapped_column(Boolean, default=False)

    task_id = mapped_column(Integer, ForeignKey('tasks.id'))
    tasks = relationship('Task', back_populates='instagram')


class Facebook(Base):
    __tablename__ = 'facebook'

    id = mapped_column(Integer, autoincrement=True, primary_key=True)
    url = mapped_column(String, nullable=False)
    username = mapped_column(String, nullable=False)
    bio = mapped_column(String)
    followers = mapped_column(Integer)
    verified = mapped_column(Boolean, default=False)

    task_id = mapped_column(Integer, ForeignKey('tasks.id'))
    tasks = relationship('Task', back_populates='facebook')

