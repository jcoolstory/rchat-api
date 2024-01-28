from typing import Union, List
from fastapi import FastAPI, WebSocket, APIRouter
from chat.models import ChatRoom, ChatRoom, CreateChatRoom, RequestChatMessage

from common.response import ErrorResponseModel, ResponseModel
from common.time import current_milli_time
from user.auth_origin import LOGIN_REQUIRE
from .ConnectionManager import manager
from .ChatManager import ChatManager
from chat import database

router = APIRouter(
    # prefix="/ws",
    tags=["ws"],
)

@router.websocket("/ws/chat/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await ChatManager.message_proc(room_id, websocket)

@router.get("/api/chatroom")
async def get_chat_rooms():
    room = await database.retrieve_room()
    return ResponseModel(room)

@router.post("/api/chatroom")
async def create_chat_room(room: CreateChatRoom):
    if room.users:
        room.users = [room.owner] + room.users
    else:
        room.users = [room.owner]
    
    result = await database.create_room(room)
    if result:
        return {"id":result}
    return []

@router.api_route("/api/chatroom/{room_id}")
async def chat_rooms(room_id:str):
    result = await database.retrieve_room_detail(room_id)
    if result:
        return ResponseModel(result)
    else:
        return ErrorResponseModel(error=404,code=404, message="존재하지 않는 대화방입니다")
    
@router.get("/api/chatroom/{room_id}/history")
async def get_chat_history(room_id: str):
    result = await database.retrieve_message(room_id)
    return ResponseModel(result)
    
    
@router.post("/api/chatroom/{room_id}/history")
async def send_chat_message(room_id: str, message: RequestChatMessage):
    message.roomId = room_id
    message.timestamp = current_milli_time()
    result = await database.create_message(message)
    return ResponseModel(result)
    
@router.post("/api/chatroom/{room_id}/enter")
async def chat_rooms(room_id: str):
    if  room_id in chatHistory_data:
        return chatHistory_data[room_id]
    else :
        return []

@router.post("/api/chatroom/{room_id}/exit")
async def chat_rooms(room_id: str):
    if  room_id in chatHistory_data:
        return chatHistory_data[room_id]
    else :
        return []
    

@router.get("/api/admin/chatroom")
async def get_user_list(user: LOGIN_REQUIRE):
    retrieve_user = await database.retrieve_user()
    if retrieve_user:
        return ResponseModel(retrieve_user, "Student data retrieved successfully")


@router.get("/api/admin/chatroom/{id}")
async def get_user_list(id:str, user: LOGIN_REQUIRE):
    retrieve_user = await database.get_user_info(id)
    if retrieve_user:
        return ResponseModel(retrieve_user, "Student data retrieved successfully")


@router.delete("/api/admin/chatroom/{id}")
async def delete_room(id:str, user: LOGIN_REQUIRE):
    delete_room = await database.delete_room(id)
    if delete_room:
        return ResponseModel(delete_room, "Student data retrieved successfully")
    else:
        return ResponseModel(delete_room, "Student data retrieved successfully")
