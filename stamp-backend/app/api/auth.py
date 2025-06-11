from fastapi import APIRouter, Header, HTTPException, status, Depends, Form
from pydantic import BaseModel
from models.User import User
from helpers.password_manager import encrypt_password, verify_password
from helpers.jwt import generate_token, authorise_user
from typing import Annotated

class UserItem(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str


class LoginBody(BaseModel):
    email: str
    password: str


def get_current_user(authorisation: str = Header(...)):
    if not authorisation.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorisation header"
        )
    token = authorisation.split(" ")[1]
    payload = authorise_user(token)
    return payload

router = APIRouter(prefix='/auth')

@router.post('/register')
async def create_user(user: Annotated[UserItem, Form(...)]):
    user = User.objects(email=user.email).first()
    if user:
        print(user)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with email already exists"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=encrypt_password(user.password),
        first_name=user.first_name,
        last_name=user.last_name
        )
    new_user.save()

    token = generate_token({"id": str(new_user.id)})

    return {
        "user": {
            "username": new_user.username,
            "email": new_user.email,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name
        },
        "token": token
    }
@router.post('/login')
async def login(body: Annotated[LoginBody, Form(...)]):
    user = User.objects(email=body.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with email not found"
        )
    if not verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect credentials"
        )
    token = generate_token({"id": str(user.id)})
    return {
        "user": {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        },
        "token": token
    }

@router.get('/me')
async def get_me(current_user=Depends(get_current_user)):
    return {"user": current_user}
