from sqlalchemy.orm import Session
from . import schema, models


def error_message(message):
    return {
        'error': message
    }


def get_user(db: Session, user_id: str = None):
    if user_id is None:
        return db.query(models.User).all()
    else:
        return db.query(models.User).filter(models.User.id == user_id).first()


def save_user(db: Session, user: schema.User):
    user_model = models.User(**user.dict())
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return {"message": "user created successfully"}
