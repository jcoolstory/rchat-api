import motor.motor_asyncio
from passlib.context import CryptContext
from config import db, engine
from user.models import UserSchema
from pymongo.results import InsertOneResult, DeleteResult, UpdateResult

# MongoDB 연결
user_collection = db.get_collection("user")

# password 암호화 모듈
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# password 비교
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# password 암호화
def hash_password(password):
    return pwd_context.hash(password)


# DB 에서 User 정보 가져오기
async def get_user_info(id: str):
    user_info = await user_collection.find_one({"id":id})
    if user_info:
        return user_info
    
async def create_user_info(user: UserSchema):
    result : InsertOneResult = await user_collection.insert_one(user.model_dump())
    return result.inserted_id


async def retrieve_user():
    users = []
    async for user in user_collection.find():
        user['_id'] = str(user['_id'])
        users.append(user)
    return users

async def delete_user(id:str):
    result : DeleteResult = await user_collection.delete_one({"id":id})
    return result.deleted_count

async def update_user(id:str, user:UserSchema):
    result: UpdateResult = await user_collection.update_one({"id": id}, {"$set": user.model_dump()})
    
    return result