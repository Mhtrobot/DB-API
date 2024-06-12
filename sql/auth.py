
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal

SECRET_KEY = "YOMAMAAHOE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    if expires_delta is None:
        expires_delta = timedelta(minutes=2)
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(SessionLocal)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        token_data = verify_token(token, credentials_exception)
    except JWTError:
        raise credentials_exception
    user = db.query(models.USER).filter(models.USER.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user
