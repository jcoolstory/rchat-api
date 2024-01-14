from typing import List, Optional
from pydantic import BaseModel
from typing import Union

class TrType:
    chatroom = "chatroom"
    cmd = "cmd"
    enter = "enter_room"
    exit = "exit_room"
    private_message = "pm"

class MessageType:
    text = "text"
    file = "file"

class ChatRoom(BaseModel):
    id: int
    name: str
    description: str
    type: str
    users: List[str] = []
    owner: str


class CreateChatRoom(BaseModel):
    name: str
    description: str
    users: List[str] = []
    owner: str
    type: str

class ChatMessage(BaseModel) :
    roomId: str
    timestamp: Optional[int]
    sender: str
    to: Optional[str] = None
    message: str


class TrData(BaseModel): 
    type: str
    subType: str
    content: Union[ChatMessage,object, str]


class RequestChatMessage(BaseModel) :
    roomId: Optional[str] = None 
    timestamp: Optional[int] = None
    sender: str
    to: Optional[str] = None
    message: str
