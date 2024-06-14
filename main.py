from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException,status
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated, List
from sql import models, schemas, auth
from sql.database import SessionLocal, engine, get_db

app = FastAPI()


@app.get('/')
def read_root():
    return {'Hello': 'World'}

@app.get('/users')
def read_users(limit: int, db: Annotated[Session, Depends(get_db)]):
    return db.query(models.USER).limit(limit).all()

@app.get('/users/{user_id}', response_model=schemas.UserBase)
def read_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.query(models.USER).filter(models.USER.user_id == user_id).first()
    return user

@app.post('/register/user')
def create_user(user: schemas.UserBase, db: Annotated[Session, Depends(get_db)]):
    isTaken = db.query(models.USER).filter(models.USER.phone == user.phone).first()
    if isTaken:
        raise HTTPException(status_code=404, detail=f"User with phone {user.phone} already exists")

    db_user = models.USER(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post('/login-token')
def login_for_access_token(db: Annotated[Session, Depends(get_db)], form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.USER).filter(models.USER.email == form_data.username, models.USER.phone == form_data.password).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
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
        "access_token": access_token, "token_type": "bearer"
    }

@app.get("/loged-user", response_model=schemas.UserBase)
def get_current_user(current_user: models.USER = Depends(auth.get_current_user)):
    return current_user

@app.put('/user-update/{user_id}', response_model=schemas.UserUpdate)
def update_user(user_id: int, user: schemas.UserUpdate, db: Annotated[Session, Depends(get_db)]):
    db_user = db.query(models.USER).filter(models.USER.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="User not found")
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/delete-users/{user_id}", response_model=schemas.UserBase)
def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)], current_user: models.USER = Depends(auth.get_current_user)):
    db_user = db.query(models.USER).filter(models.USER.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if db_user.email != current_user.email or db_user.phone != current_user.phone:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to take action")
    db.delete(db_user)
    db.commit()
    return {
        "message": "User deleted",
        "user": db_user
    }

'''
app.openapi_schema = None
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title='DB-API',
        version='1.0.0',
        description='Renting House System API',
        routes=app.routes
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
'''

