from fastapi import FastAPI
from sql.database import SessionLocal

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