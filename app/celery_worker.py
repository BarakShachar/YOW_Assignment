from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from . import models

celery = Celery(__name__)
celery.conf.broker_url = "redis://redis:6379/0"
celery.conf.result_backend = "redis://redis:6379/0"
db_uri = "postgresql://username:password@db:5432/db"


session = scoped_session(sessionmaker())


@celery.task(name="create_task")
def create_task(user_email: str, user):
    engine = create_engine(db_uri)
    session.configure(bind=engine)
    session.query(models.User).filter(models.User.email == user_email).update(user, synchronize_session=False)
    session.commit()
    session.close()
    return "user updated"
