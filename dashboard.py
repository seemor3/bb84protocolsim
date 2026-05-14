from fastapi import FastAPI, WebSocket
from typing import List
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

connected_clients: List[WebSocket] = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for client in connected_clients:
                if client != websocket:
                    await client.send_text(data)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        connected_clients.remove(websocket)

@app.get("/")
async def get():
    return {"message": "Welcome to the dashboard!"}

