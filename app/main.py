from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/user/', status_code=status.HTTP_201_CREATED)
def save_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    user_in_db = crud.get_user_by_email(db, user.email)
    if user_in_db:
        raise HTTPException(status_code=400, detail=crud.error_message('This email already exists'))
    return crud.save_user(db, user)


@app.get('/user/{user_email}/', response_model=schemas.User)
def save_user(user_email: str, db: Session = Depends(get_db)):
    user_info = crud.get_user_by_email(db, user_email)
    if user_info is None:
        raise HTTPException(400, detail=crud.error_message('no user found for user_email {}'.format(user_email)))
    return user_info


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip, limit)
    return users


@app.patch('/user/{user_email}/')
def change_user_info(user_email: str, user: schemas.User, db: Session = Depends(get_db)):
    updated_user = crud.update_user_info(db, user_email, user)
    if updated_user is None:
        raise HTTPException(400, detail=crud.error_message('no user found for user_email {}'.format(user_email)))
    return {"message": "user updated successfully"}


@app.delete('/user/{user_email}/')
def delete_user(user_email: str, db: Session = Depends(get_db)):
    deleted_user = crud.delete_user(db, user_email)
    if deleted_user is None:
        raise HTTPException(400, detail=crud.error_message('no user found for user_email {}').format(user_email))
    return deleted_user
