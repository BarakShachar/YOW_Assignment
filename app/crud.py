from sqlalchemy.orm import Session
from . import schemas
from . import models
from .celery_worker import create_task


def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()


def save_user(db: Session, user: schemas.UserBase):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def update_user_info(db: Session, user_email: str, user: schemas.UserUpdate) -> str | None:
    old_user = db.query(models.User).filter(models.User.email == user_email)
    if user.email is not None:
        email_exist = db.query(models.User).filter(models.User.email == user.email).first()
        if email_exist is not None:
            return f'the email {user.email} already exist'
    if old_user.first() is None:
        return f'no user found for user_email {user_email}'
    task = create_task.delay(user_email, user.dict(exclude_unset=True))
    return None


def delete_user(db: Session, user_email: str):
    db_user = db.query(models.User).filter(models.User.email == user_email).first()
    if db_user is None:
        return None
    db.delete(db_user)
    db.commit()
    return True
