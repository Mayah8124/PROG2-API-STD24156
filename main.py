import json
from fastapi import FastAPI
from starlette.responses import Response
from typing import List

app = FastAPI()


class SecretPayload(BaseModel):
    secret_code: int = 12345678

@app.get("/")
def root(request: Request):
    accept_header = request.headers.get("accept")
    auth_header = request.headers.get("x-api-key")

    if auth_header != "12345678":
        return JSONResponse(
            status_code=403,
            content={"error": "API key not recognized"}
        )
    return Response(content=html_content, status_code=200, media_type="text/html")

    if accept_header not in ["text/html", "text/plain"]:
        return JSONResponse(content={'Bad Request'}, status_code=400)


    with open("welcome.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=200, media_type="text/html")


@app.get("/{full_path:path}")
def catch_all(full_path: str):
    with open("new.html", "r", encoding="utf-8") as file
        html_content= file.read()
    return Response(content=html_content, status_code=404, media_type="text/html")


events_store: List[EventModel] = []

class EventModel(BaseModel):
    name: str
    description: str
    start_date: str
    end_date: str


def serialized_stored_events():
    events_converted = []
    for event in events_store:
        events_converted.append(event.model_dump())
    return events_converted


@app.get("/events")
def list_events():
return {"events": serialized_stored_events()}


@app.post("/events")
def add_events(new_events: List[EventModel]):
    events_store.extend(new_events)
    return {"events": serialized_stored_events()}


@app.put("/events")
def update_events(updated_events: List[EventModel]):

    for updated_event in updated_events:
        found = False
        for stored_event in events_store:
            if stored_event.name == updated_event.name:
                i = events_store.index(stored_event)
                events_store.remove(stored_event)
                events_store.insert(i, updated_event)
                found = True
                break
        if not found:
            events_store.append(updated_event)

    return {"events": serialized_stored_events()}

