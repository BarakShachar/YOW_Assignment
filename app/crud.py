from sqlalchemy.orm import Session
from . import schemas, models


def error_message(message):
    return {
        'error': message
    }


def get_user_by_email(db: Session, user_email: str = None):
    if user_email is None:
        return db.query(models.User).all()
    else:
        return db.query(models.User).filter(models.User.email == user_email).first()


def save_user(db: Session, user: schemas.UserBase):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "user created successfully"}


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def update_user_info(db: Session, user_email: str, user: schemas.User):
    old_user = db.query(models.User).filter(models.User.email == user_email)
    if old_user.first() is None:
        return None
    old_user.update(user.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return old_user.first()


def delete_user(db: Session, user_email: str):
    db_user = db.query(models.User).filter(models.User.email == user_email).first()
    if db_user is None:
        return None
    db.delete(db_user)
    db.commit()
    return {"message": "user deleted successfully"}
