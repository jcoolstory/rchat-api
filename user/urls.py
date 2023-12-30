from typing import Union, List
from fastapi import FastAPI, APIRouter
from datetime import datetime
from common.response import ErrorResponseModel, ResponseModel
from user.models import UserSchema, UserUpdateSchema
from user import database
from user.models import UserJoinSchema, UserLoginSchema

router = APIRouter(
    # prefix="/ws",
    tags=["user"],
)

@router.post("/api/user/login")
async def login(data:UserLoginSchema):

    return None
    
@router.post("/api/user/join")
async def join(data:UserJoinSchema):
    if data.password != data.password_repeat:
        return ErrorResponseModel(error=500, code=200, message="비밀번호가 일치하지 않습니다")
    
    user = await database.get_user_info(data.id)
    if user:
        return ErrorResponseModel(error=500, code=200, message="이미 가입된 유저입니다.")
    
    data.password = database.hash_password(password=data.password)
    user_data = UserSchema(**data.model_dump())
    result = await database.create_user_info(user_data)
    if result:
        return ResponseModel({"id":data.id})

@router.put("/api/user/{id}")
async def update_user(id: str, data: UserUpdateSchema):
    result = await database.update_user(id,data)
    return ResponseModel(result.modified_count)

@router.get("/api/admin/user")
async def get_user_list():
    retrieve_user = await database.retrieve_user()
    if retrieve_user:
        return ResponseModel(retrieve_user, "Student data retrieved successfully")

@router.delete("/api/admin/user/{id}")
async def delete_user(id:str):
    delete_user = await database.delete_user(id)
    if delete_user:
        return ResponseModel(delete_user, "Student data retrieved successfully")
    else:
        return ResponseModel(delete_user, "Student data retrieved successfully")
