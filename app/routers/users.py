from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from ..models import Users
from .auth import get_current_user, bcrypt_context
from pydantic import BaseModel, Field


class UserRead(BaseModel):
    username: str 
    email: str 
    first_name: str
    last_name: str 
    role: str
    phone_number: str

    class Config:
        from_attributes = True


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


router = APIRouter(
    prefix='/user',
    tags=['user']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

user_dependecy = Annotated[dict, Depends(get_current_user)]


@router.get('/me', status_code=status.HTTP_200_OK, response_model=UserRead)
async def read_user(user: user_dependecy, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put('/change_password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependecy, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Passwords not matching')
    
    user_model.hashed_password=bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()

@router.put('/change_phonenumber/{phone_number}', status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependecy, db: db_dependency, phone_number: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    user_model.phone_number=phone_number
    db.add(user_model)
    db.commit()
