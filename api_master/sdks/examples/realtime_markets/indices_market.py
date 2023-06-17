import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from polygon.websocket import WebSocketMessage, WebSocketClient, Market
from polygon.websocket import WebSocketClient
from polygon.websocket.models import WebSocketMessage
from typing import List
import asyncio

from api_master.cfg import YOUR_API_KEY
from sdks.polygon_sdk.async_polygon_sdk import AsyncPolygonSDK

poly = AsyncPolygonSDK(YOUR_API_KEY)
c = WebSocketClient(subscriptions=["V.*"], market=Market.Indices, api_key=YOUR_API_KEY) #connect to the crypto market and subscribe to trades and quotes


async def handle_msg(msgs: List[WebSocketMessage]):
    for m in msgs:
        print(m)




async def main():
    await asyncio.gather(c.connect(handle_msg))


asyncio.run(main())