import threading
from typing import List

from fastapi import FastAPI, Request, Response
from pydantic import BaseModel


class Node(BaseModel):
    address: str
    id: int


class ViewBody(BaseModel):
    defaultShard: List[Node]


class KVStore:
    def __init__(self):
        self._dict: dict[str, str] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Response:
        with self._lock:
            value = self._dict.get(key)
        if value is None:
            return Response(status_code=404)
        return Response(content=value, status_code=200)

    def put(self, key: str, value: str) -> Response:
        with self._lock:
            self._dict[key] = value
        return Response(status_code=200)


app = FastAPI()
store = KVStore()
view = {}


@app.get("/ping")
def get_ping():
    return Response(status_code=200)


@app.put("/view")
def put_view(body: ViewBody):
    global view
    view = body.model_dump()
    return Response(status_code=200)


@app.put("/data/")
async def put_data_empty(request: Request):
    body = await request.body()
    return store.put("", body.decode())


@app.get("/data/")
def get_data_empty():
    return store.get("")


@app.put("/data/{key}")
async def put_data(key: str, request: Request):
    body = await request.body()
    return store.put(key, body.decode())


@app.get("/data/{key}")
def get_data(key: str):
    return store.get(key)
