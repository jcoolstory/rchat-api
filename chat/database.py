from passlib.context import CryptContext
from chat.models import RequestChatMessage
from common.time import current_milli_time
from config import db, engine
from user.models import UserSchema
from pymongo.results import InsertOneResult, DeleteResult, UpdateResult

from bson.objectid import ObjectId

# MongoDB 연결
room_collection = db.get_collection("room")
message_collection = db.get_collection("message")
    
async def create_room(room: UserSchema):
    result : InsertOneResult = await room_collection.insert_one(room.model_dump())
    return str(result.inserted_id)

async def retrieve_room():
    rooms = []
    async for room in room_collection.find():
        room['_id'] = str(room['_id'])
        rooms.append(room)
    return rooms

async def retrieve_room_detail(id:str):
    room = await room_collection.find_one({"_id": ObjectId(id)})
    room['_id'] = str(room['_id'])
    room['id'] = room['_id']
    return room

async def delete_room(id:str):
    result : DeleteResult = await room_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count

async def update_room(id:str, room:UserSchema):
    result: UpdateResult = await room_collection.update_one({"_id": ObjectId(id)}, {"$set": room.model_dump()})
    return result


async def create_message(tr: RequestChatMessage):
    result: InsertOneResult = await message_collection.insert_one(tr.model_dump())
    return { "inserted_id": str(result.inserted_id)}

async def retrieve_message(id: str, page: int = 100):
    result = message_collection.find({"roomId":id } ).sort('timestamp', -1).limit(page)
    messages = []
    async for message in result:
        message['_id'] = str(message['_id'])
        messages.append(message)
    return messages