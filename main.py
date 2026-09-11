import character_generator

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.get("/")
def home():
    return FileResponse("index.html")

@app.get("/game")
def game():
    return FileResponse("game-page.html")

@app.get("/script.js")
def javascript():
    return FileResponse("script.js")

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