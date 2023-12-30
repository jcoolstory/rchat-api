from chat.database import create_message, retrieve_room_detail
from common.time import current_milli_time
from .ConnectionManager import ConnectionManager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from .ConnectionManager import manager
import json, os
from chat.models import ChatRoom, RequestChatMessage, TrData, TrType

curpath = os.path.abspath(".")
mock_chat_room_path = os.path.join(curpath, "chat/mocks/rooms.json")
mock_chat_chatHistory_path = os.path.join(curpath, "chat/mocks/chatHistory.json")

chat_room_data = {}

with open(mock_chat_room_path) as f:
    chat_room_data = json.load(f)

with open(mock_chat_chatHistory_path) as f:
    chatHistory_data = json.load(f)


def get_room(room_id):
    find_room = [ x for x in chat_room_data if x['id'] == room_id ] 
    if  find_room:
        return find_room[0]
    return None

class ChatManager:
    def __init__(self):
        pass

    @staticmethod
    async def message_handler(websocket:WebSocket, data:str):
        trData = TrData(**json.loads(data))
        if trData.type == TrType.cmd:
            if trData.content["cmd"] == "connect":
                manager.add_user(websocket, trData.content["id"])
        elif trData.type == TrType.chatroom: 
            message = RequestChatMessage(**trData.content["message"], timestamp=current_milli_time())
            cur_room : ChatRoom = await retrieve_room_detail(message.roomId)
            targets = [websocket]
            for user in cur_room["users"]:
               sock = manager.get_socket_by_id(user)
               targets += sock
            targets = set(targets)
            
            await create_message(message)
            await manager.broadcast_target(trData.model_dump_json(), targets)
        elif trData.type == TrType.private_message:
            user = trData.content["to"]
            sock = manager.get_socket_by_id(user)
            if sock:
                await manager.send_personal_message(trData.model_dump_json(),sock[0])
            else:
                await manager.send_personal_message(trData.model_dump_json(),sock[0])

    @staticmethod
    async def message_proc(room_id: str, websocket: WebSocket):
        await manager.connect(websocket)

        try:
            while True:
                data = await websocket.receive_text()
                await ChatManager.message_handler(websocket, data)
                
        except WebSocketDisconnect:
            manager.disconnect(websocket)
            message = {"clientId":room_id,"message":"Offline"}
            trData = TrData(type="cmd", subType="", content=message)
            await manager.broadcast(trData.model_dump_json())


if __name__ == "__main__" :
    print (curpath)