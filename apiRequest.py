from typing import Optional

from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def root():
    return  ["71", "78", "39", "166"]


