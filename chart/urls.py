from typing import Union, List
from fastapi import FastAPI, WebSocket, APIRouter
from chat.models import ChatRoom, ChatRoom, CreateChatRoom, RequestChatMessage

from common.response import ErrorResponseModel, ResponseModel
from common.time import current_milli_time
import yfinance as yf
router = APIRouter(
    # prefix="/ws",
    tags=["chart"],
)

@router.get("/api/chart/historicals/{ticker}")
async def get_user_list(ticker:str):
    msft = yf.Ticker(ticker)
    hist = msft.history(period="1mo")
    # hist.to_json(orient='split')
    hist = hist.reset_index()
    data = hist.to_dict(orient='records')
     # hist.to_json(orient='table')
    # data = hist.to_dict(orient='columns')
    return ResponseModel(data)
    # return data