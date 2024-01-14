from typing import Union, List
from fastapi import Depends, FastAPI, APIRouter, HTTPException
from datetime import datetime
from common.response import ErrorResponseModel, ResponseModel
from user.auth_origin import create_access_token, hash_password, verify_password
from user.models import TokenSchema, UserCreateSchema, UserSchema, UserUpdateSchema
from user import database
from user.models import UserJoinSchema, UserLoginSchema
from .auth_origin import LOGIN_REQUIRE, get_current_user, oauth2_scheme

from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated

router = APIRouter(
    # prefix="/ws",
    tags=["user"],
)

@router.post("/api/user/login")
async def login(data:UserLoginSchema):
    user = await database.get_user_info(data.id)
    if user and verify_password(data.password, user["password"]):
        access_token = create_access_token(data={"sub": data.id} )
        return ResponseModel({"result":"success", "access_token": access_token, "token_type": "bearer"})

    raise HTTPException(status_code=401, detail={"code": 401, "message": "로그인정보가 일치하지 않습니다."})

@router.post("/api/token")
async def login2(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await database.get_user_info(form_data.username)
    if user and verify_password(form_data.password, user["password"]):
        access_token = create_access_token(data={"sub": form_data.username} )
        return {"access_token": access_token, "token_type": "bearer"}

    return ErrorResponseModel(error=500, code=200, message="로그인정보가 일치하지 않습니다.")


@router.post("/api/user/join")
async def join(data:UserJoinSchema):
    if data.password != data.password_repeat:
        return ErrorResponseModel(error=500, code=200, message="비밀번호가 일치하지 않습니다")
    
    user = await database.get_user_info(data.id)
    if user:
        return ErrorResponseModel(error=500, code=200, message="이미 가입된 유저입니다.")
    
    data.password = hash_password(password=data.password)
    user_data = UserCreateSchema(**data.model_dump())
    result = await database.create_user_info(user_data)
    if result:
        return ResponseModel({"id":data.id})

@router.put("/api/user/{id}")
async def update_user(id: str, data: UserUpdateSchema):
    result = await database.update_user(id,data)
    return ResponseModel(result.modified_count)

@router.get("/api/userme")
async def get_user_list(user: LOGIN_REQUIRE):
    return ResponseModel(user)


@router.get("/api/admin/user")
async def get_user_list(user: LOGIN_REQUIRE):
    retrieve_user = await database.retrieve_user()
    if retrieve_user:
        return ResponseModel(retrieve_user, "Student data retrieved successfully")


@router.get("/api/admin/user/{id}")
async def get_user_list(id:str, user: LOGIN_REQUIRE):
    retrieve_user = await database.get_user_info(id)
    if retrieve_user:
        return ResponseModel(retrieve_user, "Student data retrieved successfully")


@router.delete("/api/admin/user/{id}")
async def delete_user(id:str, user: LOGIN_REQUIRE):
    delete_user = await database.delete_user(id)
    if delete_user:
        return ResponseModel(delete_user, "Student data retrieved successfully")
    else:
        return ResponseModel(delete_user, "Student data retrieved successfully")
