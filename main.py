import character_generator
import random, string
from fastapi import FastAPI, Request
from fastapi import WebSocket, WebSocketDisconnect
import json
from fastapi.staticfiles import StaticFiles
import requests
import uuid
import os
import cv2
import numpy as np
from fastapi.responses import FileResponse, Response
import importlib.metadata

print(importlib.metadata.version("ddgs"))
app = FastAPI()
rooms ={}
connections = {}
app.mount("/images", StaticFiles(directory="cached_images"), name="images")


def cache_image(image_url):
    response = requests.get(image_url, timeout=5)
    response.raise_for_status()

    filename = f"{uuid.uuid4()}.jpg"
    filepath = os.path.join("cached_images", filename)

    image_array = np.frombuffer(response.content, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5
    )

    if len(faces) > 0:
        x, y, w, h = max(
            faces,
            key=lambda face: face[2] * face[3]
        )

        image_height, image_width = image.shape[:2]

        crop_width = image_width
        crop_height = int(crop_width * 15 / 9)

        if crop_height > image_height:
            crop_height = image_height
            crop_width = int(crop_height * 9 / 15)

        face_center_x = x + w // 2

        left = face_center_x - crop_width // 2

        left = max(
            0,
            min(left, image_width - crop_width)
        )

        face_center_y = y + h // 2

        top = face_center_y - int(crop_height * 0.30)

        top = max(
            0,
            min(top, image_height - crop_height)
        )

        image = image[
            top:top + crop_height,
            left:left + crop_width
        ]

    cv2.imwrite(filepath, image)

    return f"/images/{filename}"

@app.get("/blur-image/{filename}")
def blur_image(filename: str):
    filepath = os.path.join("cached_images", filename)

    image = cv2.imread(filepath)

    padding = 20

    padded = cv2.copyMakeBorder(
        image,
        padding, padding,
        padding, padding,
        cv2.BORDER_REPLICATE
    )

    blurred = cv2.blur(padded, (1000, 1000))

    blurred = blurred[
        padding:-padding,
        padding:-padding
    ]

    _, buffer = cv2.imencode(".jpg", blurred)

    return Response(
        content=buffer.tobytes(),
        media_type="image/jpeg"
    )

@app.get("/")
def home():
    return FileResponse("index.html")

@app.get("/script.js")
def javascript():
    return FileResponse("script.js")





@app.get("/room/{room_id}")
def get_room(room_id: str):
    return rooms[room_id]


def create_room():
    room_id = ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=5)
    )  


    rooms[room_id] = {
        "room_id": room_id,
        "players": [],
        "number_of_players": 0,
        "images":[]
    }

    return room_id


# @app.get("/join/{room_id}")
# def join_room(room_id: str):
#     if room_id not in rooms:
#         return {"error": "Room does not exist"}

#     rooms[room_id]["players"].append("player")
#     image, char_name = character_generator.get_image()
#     rooms[room_id]["images"].append()
#     return {
#         "room_id": room_id,
#         "players": len(rooms[room_id]["players"])
#     }

@app.get("/create-game")
def create_game():
    room_id = create_room()
    return {"room_id": room_id}

@app.get("/does-room-exist")
def does_room_exist(room_id: str):
    if room_id not in rooms:

        return { "exists": False, "room_id": room_id }
    return { "exists": True, "room_id": room_id}

@app.get("/game/{room_id}")
def game(room_id: str, request: Request, username: str):
    if room_id not in rooms:
        return {"error": "Room does not exist"}

    response = FileResponse("game-page.html")

    player_id = request.cookies.get(f"player_{room_id}")
    if not player_id:
        player_id = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=5)
        )

        response.set_cookie(
            key=f"player_{room_id}",
            value=player_id,
            max_age=60 * 60 * 24 * 30
        )

    response.set_cookie(
        key=f"username_{room_id}",
        value=username,
        max_age=60 * 60 * 24 * 30
    )

    return response


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()

    player_id = websocket.cookies.get(f"player_{room_id}")
    username = websocket.cookies.get(f"username_{room_id}")

    if not player_id:
        player_id = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=5)
        )

    existing_player = None

    for entry in rooms[room_id]["images"]:
        if entry["player_id"] == player_id:
            existing_player = entry
            break

    if existing_player is None:

        image_url, char_name = character_generator.get_image()
        image = cache_image(image_url)
        image_entry={
            "player_id": player_id,
            "username": username,
            "name": char_name,
            "image": image
        }

        rooms[room_id]["images"].append(image_entry)
        rooms[room_id]["players"].append(player_id)
        rooms[room_id]["number_of_players"] += 1

        print("NEW PLAYER:", player_id)
        print("CHARACTER:", char_name)


    else:

        print("RECONNECTING PLAYER:", player_id)
        print("CHARACTER:", existing_player["name"])


    if room_id not in connections:
        connections[room_id] = []

    connections[room_id] = [
        connection
        for connection in connections[room_id]
        if connection["player_id"] != player_id
    ]

    connections[room_id].append({
        "websocket": websocket,
        "player_id": player_id
    })


    for connection in connections[room_id].copy():

        room_players = []

        for entry in rooms[room_id]["images"]:
            room_players.append({
                "player_id": entry["player_id"],
                "username": entry["username"],
                "name": entry["name"],
                "image": entry["image"]
            })

        try:
            await connection["websocket"].send_text(json.dumps({
                "type": "room_state",
                "players": room_players,
                "your_player_id": connection["player_id"]
            }))

        except Exception:
            if connection in connections[room_id]:
                connections[room_id].remove(connection)

    try:

        while True:

            data = await websocket.receive_text()

            for connection in connections[room_id].copy():

                try:
                    await connection["websocket"].send_text(data)

                except Exception:

                    if connection in connections[room_id]:
                        connections[room_id].remove(connection)

    except WebSocketDisconnect:

        connections[room_id] = [
            connection
            for connection in connections[room_id]
            if connection["websocket"] != websocket
        ]
@app.get("/style.css")
def css():
    return FileResponse("style.css")

@app.get("/CFBitronikDemo-Regular.ttf")
def font():
    return FileResponse("CFBitronikDemo-Regular.ttf")

@app.get("/return-character/{room_id}")
def return_character(room_id: str, player_id: str):
    print(rooms[room_id]["images"][player_id]["image"])
    return rooms[room_id]["images"][player_id]["image"]