import json
from urllib.request import Request
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from starlette.responses import Response
from typing import List

app = FastAPI()

#1st Question
@app.get("/hello")
def hello():
    with open("hello.html", "r", encoding="utf-8") as file:
        html_content = file.read()
        return Response(
            content=html_content,
            status_code=200,
            media_type="text/html"
        )

#2nd Question
@app.get("/welcome")
def welcome(name: str):
    return Response(
        content=json.dumps({"message": f"Welcome {name}"}),
        status_code=200,
        media_type="application/json"
    )

class Player(BaseModel):
    Number : int
    Name : str

player_list: List[Player] = []

def serialized_player_list():
    player_list_converted = []
    for player in player_list:
        player_list_converted.append(player.model_dump())
    return player_list_converted

#3rd Question
@app.post("/players")
def post_players(new_player_list: List[Player]):
    for new_player in new_player_list:
        player_list.append(new_player)
    serialized_players = serialized_player_list()
    return Response(
        content=json.dumps({"players": serialized_players}),
        status_code=201,
        media_type="application/json"
    )

#4th Question
@app.get("/players")
def get_players():
    return Response(
        content=json.dumps({"players":serialized_player_list()}),
        status_code=200,
        media_type="application/json"
    )

#5th Question
@app.put("/players")
async def update_players(new_player_list : List[Player]):
    for updated_player in new_player_list:
        found = False
        for stored_player in player_list:
            if stored_player.Number == updated_player.Number:
                i = player_list.index(stored_player)
                player_list[i] = updated_player
                player_list.insert(i, updated_player)
                found = True
                break
        if not found:
            player_list.append(updated_player)
    return Response(
        content=json.dumps({"players":serialized_player_list()}),
        status_code=200 ,
        media_type="application/json"
    )

#6th question
#in the postman file

#Bonus Question
@app.get("/players-authorized")
def update_player_list(request: Request):
    authorization_value = request.headers.get("Authorization")
    if authorization_value is None:
        return Response(
            content=json.dumps({"message": "You are not authorized to have access to the demanded resource."}),
            status_code=401,
            media_type="application/json"
        )
    elif authorization_value != "bon courage":
        return Response(
            content=json.dumps({"message": "You do not have the necessary permissions to access the demanded resource"}),
            status_code=403,
            media_type="application/json"
        )
    else:
        return Response(
            content=json.dumps({"players": serialized_player_list()}),
            status_code=200,
            media_type="application/json"
        )