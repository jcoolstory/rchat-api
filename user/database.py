import motor.motor_asyncio
from passlib.context import CryptContext
from config import db, engine
from user.models import UserCreateSchema, UserSchema
from pymongo.results import InsertOneResult, DeleteResult, UpdateResult

# MongoDB 연결
user_collection = db.get_collection("user")



# DB 에서 User 정보 가져오기
async def get_user_info(id: str) -> UserSchema: 
    user_info = await user_collection.find_one({"id":id})
    return user_info
    
async def create_user_info(user: UserCreateSchema):
    result : InsertOneResult = await user_collection.insert_one(user.model_dump())
    return result.inserted_id

async def retrieve_user():
    users = []
    async for user in user_collection.find():
        users.append(UserSchema(**user))
    return users

async def delete_user(id:str):
    result : DeleteResult = await user_collection.delete_one({"id":id})
    return result.deleted_count

async def update_user(id:str, user:UserSchema):
    result: UpdateResult = await user_collection.update_one({"id": id}, {"$set": user.model_dump()})
    
    return result