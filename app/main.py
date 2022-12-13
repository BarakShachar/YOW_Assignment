from fastapi import FastAPI, Depends, HTTPException
from .database import SessionLocal, engine
from .schema import User
from . import crud, models
app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post('/user')
def save_user(user: User, db=Depends(db)):
    user_in_db = crud.get_user(db, user.id)
    if user_in_db:
        raise HTTPException(400, detail=crud.error_message('This user already exists'))
    return crud.save_user(db, user)


@app.get('/user/{user_id}')
def save_user(user_id: str, db=Depends(db)):
    user_info = crud.get_user(db, user_id)
    if user_info:
        return user_info
    else:
        raise HTTPException(400, detail=crud.error_message('no user found for user_id {}').format(user_id))

@app.patch('/user/{user_id}')
def change_user_info(user_id: str, db=Depends(db)):
    pass
