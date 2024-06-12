from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sql import models, schemas
from sql.database import SessionLocal, engine

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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