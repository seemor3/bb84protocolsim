from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

connected_clients: List[WebSocket] = []

'''class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None'''

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for client in connected_clients:
                if client != websocket:
                    await client.send_text(f"Message from client: {data}")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        connected_clients.remove(websocket)
'''
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}'''