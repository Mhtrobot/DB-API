from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated, List
from sql import models, schemas, auth
from sql.database import SessionLocal, engine

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[SessionLocal, Depends(get_db)]

@app.get('/')
def read_root():
    return {'Hello': 'World'}

@app.get('/users')
def read_users(limit: int, db: Session = Depends(get_db)):
    return db.query(models.USER).limit(limit).all()

@app.post('/register/user')
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    isTaken = db.query(models.USER).filter(models.USER.phone == user.phone).first()
    if isTaken:
        raise HTTPException(status_code=404, detail=f"User with phone {user.phone} already exists")

    db_user = models.USER(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post('/login-token')
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.USER).filter(models.USER.email == form_data.username, models.USER.phone == form_data.password).first()
    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or phone",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {
        "message": "Login Successful",
        "user_detail": user,
        "access_token": access_token, "token_type": "bearer"}

@app.get("/users/current", response_model=schemas.UserBase)
def get_current_user(current_user: models.USER = Depends(auth.get_current_user)):
    return current_user

@app.put('/user-update/${user_id}', response_model=schemas.UserUpdate)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.USER).filter(models.USER.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="User not found")
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

