import character_generator
import random, string
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi import WebSocket, WebSocketDisconnect


app = FastAPI()
rooms ={}
connections = {}

@app.get("/")
def home():
    return FileResponse("index.html")

@app.get("/script.js")
def javascript():
    return FileResponse("script.js")


def create_room():
    room_id = ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=5)
    )

    rooms[room_id] = {
        "players": []
    }

    return room_id


@app.get("/join/{room_id}")
def join_room(room_id: str):
    if room_id not in rooms:
        return {"error": "Room does not exist"}

    rooms[room_id]["players"].append("player")

    return {
        "room_id": room_id,
        "players": len(rooms[room_id]["players"])
    }

@app.get("/create-game")
def create_game():
    room_id = create_room()
    return {"room_id": room_id}



@app.get("/game/{room_id}")
def game(room_id: str):
    if room_id not in rooms:
        return {"error": "Room does not exist"}

    return FileResponse("game-page.html")



@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    player_id = ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=5)
    )
    rooms[room_id]["players"].append(player_id)
    await websocket.send_text(player_id)

    print("Player connected:", player_id)
    if room_id not in connections:
        connections[room_id] = []

    connections[room_id].append(websocket)
    for connection in connections[room_id]:
        await connection.send_text(
            str(rooms[room_id]["players"])
        )
    print("Player connected to room:", room_id)

    try:
        while True:
            data = await websocket.receive_text()

            for connection in connections[room_id]:
                await connection.send_text(data)

    except WebSocketDisconnect:
        connections[room_id].remove(websocket)
        rooms[room_id]["players"].remove(player_id)
        
@app.get("/style.css")
def css():
    return FileResponse("style.css")

@app.get("/CFBitronikDemo-Regular.ttf")
def font():
    return FileResponse("CFBitronikDemo-Regular.ttf")

@app.get("/random-character")
def random_character():
    image = character_generator.get_image()

    return {"image": image}