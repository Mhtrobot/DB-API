from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException,status, Header
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.orm import Session
from typing import Annotated, List, Optional
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
async def login_for_access_token(db: Annotated[Session, Depends(get_db)], form_data: OAuth2PasswordRequestForm = Depends()):
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
async def get_current_user(db: Annotated[Session, Depends(get_db)], token: str = Header(...)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.USER).filter(models.USER.email == email).first()
    if user is None:
        raise credentials_exception
    return user

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

@app.delete("/delete-user", response_model=schemas.UserBase)
async def delete_user(db: Annotated[Session, Depends(get_db)], token: str = Header(...)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    current_user = db.query(models.USER).filter(models.USER.email == email).first()
    if current_user is None:
        raise credentials_exception
        return False

    db_user = db.query(models.USER).filter(models.USER.email == current_user.email, models.USER.phone == current_user.phone).first()
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

# Add the OpenAPI customization
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


@app.get("/houses/", response_model=List[schemas.Item])
def search_houses(name: Optional[str] = None, state: Optional[str] = None, city: Optional[str] = None,
                  min_price: Optional[float] = None, max_price: Optional[float] = None, db: Session = Depends(get_db)):
    query = db.query(models.Item)

    if name:
        query = query.filter(models.Item.name.contains(name))
    if state or city:
        query = query.join(models.Location)
        if state:
            query = query.filter(models.Location.state.contains(state))
        if city:
            query = query.filter(models.Location.city.contains(city))
    if min_price is not None:
        query = query.filter(models.Item.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Item.price <= max_price)
    houses = query.all()
    return houses

@app.get("/users/{user_id}/travels", response_model=List[schemas.Reservation])
def get_travels(user_id: int, db: Session =Depends(get_db)):
    query = db.query(models.Reservation).filter(
        models.Reservation.renter_id == user_id ,
         models.Application.res_id == models.Reservation.res_id,
         models.Invoice.app_id == models.Application.app_id,
         models.Invoice.status == 'paid' and models.Application.status == 'approved'
    ).all()
    return query

@app.get('/messages/{host_id}/{sender}', response_model=List[schemas.Message])
def get_messages_of_specific_user(host_id: int, sender: int, db: Session =Depends(get_db)):
    query = db.query(models.Message).filter(models.Message.receiver_id == host_id , models.Message.sender_id == sender , models.Message.receiver_id == models.Item.owner_id).all()
    return query

@app.get('/all-messages/{host_id}', response_model=List[schemas.Message])
def get_all_messages(host_id: int, db: Session =Depends(get_db)):
    query = db.query(models.Message).filter(models.Message.receiver_id == host_id, models.Message.receiver_id == models.Item.owner_id).all()
    return query


@app.post("/create-house", response_model=schemas.Item)
def create_house(item: schemas.ItemCreate, db: Annotated[Session, Depends(get_db)]):
    if db.query(models.Item).filter(models.Item.name == item.name, models.Item.about == item.about).first():
        raise HTTPException(status_code=403, detail='Item already exists')
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.post("/favorites/add", response_model=schemas.Like)
def add_to_favorites(like: schemas.Like, db: Annotated[Session, Depends(get_db)]):
    query = db.query(models.Like).filter(models.Like.user_id == like.user_id, models.Like.item_id == like.item_id).first()
    if query:
        raise HTTPException(status_code=403, detail='this item is already favorited')
    db_like = models.Like(**like.dict())
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like