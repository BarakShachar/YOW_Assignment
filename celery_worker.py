import time

from celery import Celery
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

import models
from database import SessionLocal

celery = Celery(__name__)
celery.conf.broker_url = "redis://redis:6379/0"
celery.conf.result_backend = "redis://redis:6379/0"
db_uri = "postgresql://username:password@db:5432/db"


session = scoped_session(sessionmaker())


@celery.task(name="create_task")
def create_task(user_email: str, user):
    engine = create_engine(db_uri)
    session.configure(bind=engine)
    session.query(models.User).filter(models.User.email == user_email).update(user)
    # db.query(models.User).filter(models.User.email == user_email).update(user)
    # old_user.update(user.dict(exclude_unset=True), synchronize_session=False)
    # db.commit()
    session.commit()
    session.close()
    return "you are the king"


# @celery.task(name="create_task")
# def create_task(a, b, c):
#     time.sleep(a)
#     return b + c
