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