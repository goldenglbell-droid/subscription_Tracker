import os
import logging
from enum import Enum
from typing import Dict
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

APP_NAME = os.getenv("APP_NAME", "SubTracker")
CURRENCY = os.getenv("CURRENCY", "RUB")

app = FastAPI(title=APP_NAME)

class SubCategory(str, Enum):
    music = "music"
    video = "video"
    soft = "soft"
    other = "other"

class Subscription(BaseModel):
    name: str
    cost: float
    category: SubCategory

_db: Dict[int, Subscription] = {}
_current_id = 1

@app.get("/")
def root():
    return {"status": "running", "app": APP_NAME}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/version")
def version():
    return {"version": "0.1.0"}

@app.post("/subscriptions/", status_code=201)
def create_subscription(sub: Subscription):
    global _current_id
    _db[_current_id] = sub
    logger.info(f"Created subscription {sub.name} (ID: {_current_id})")
    
    _current_id += 1
    return {"id": _current_id - 1}

@app.get("/subscriptions/")
def get_subscriptions(category: SubCategory = None):
    if category:
        filtered = {k: v for k, v in _db.items() if v.category == category}
        return {"currency": CURRENCY, "data": filtered}
    return {"currency": CURRENCY, "data": _db}

@app.get("/subscriptions/{sub_id}")
def get_subscription(sub_id: int):
    if sub_id not in _db:
        raise HTTPException(status_code=404, detail="Not found")
    return _db[sub_id]

@app.get("/total/")
def get_total():
    total_cost = sum(sub.cost for sub in _db.values())
    return {"total": total_cost, "currency": CURRENCY}
