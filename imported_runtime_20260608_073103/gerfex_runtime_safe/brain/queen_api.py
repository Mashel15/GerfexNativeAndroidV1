from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from queen_core import queen_think

app = FastAPI(title="Gerfex Queen Runtime Safe API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ThinkRequest(BaseModel):
    prompt: str
    model: str = "Queen"
    model_state: dict = {}

@app.get("/")
def root():
    return {
        "name": "Gerfex",
        "core": "Queen",
        "status": "online",
        "source": "gerfex_runtime_safe"
    }

@app.post("/think")
def think(req: ThinkRequest):
    return queen_think(req.prompt, req.model, req.model_state or {})
