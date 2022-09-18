from pathlib import Path
from fastapi import FastAPI, BackgroundTasks
from fastapi.requests import Request
from config import Config
from assets_updater import AssetsUpdater
from os import listdir
from re import match

app = FastAPI()
ROOT = Config.ROOT


@app.post("/api/force_update")
def _(request: Request, background_tasks: BackgroundTasks):
    if request.headers.get("Authorization") == Config.token:
        background_tasks.add_task(AssetsUpdater.update)
        return {"message": "Succeeded."}
    return {"message": "Access denied."}


@app.get("/api/song_list")
def _(request: Request):
    resp_json = {}
    for song_id in listdir(ROOT / "assets" / "songs"):
        if not Path.is_file(ROOT / "assets" / "songs" / song_id):
            resp_json[song_id] = [
                f"{Config.base_url or request.base_url}assets/songs/{song_id}/{file}"
                for file in listdir(ROOT / "assets" / "songs" / song_id)
                if match(r"(base|[0123]).jpg", file)
            ]
    return resp_json


@app.get("/api/char_list")
def _(request: Request):
    resp_json = {}
    for file in listdir(ROOT / "assets" / "char"):
        resp_json[file] = f"{Config.base_url or request.base_url}assets/char/{file}"
    return resp_json
