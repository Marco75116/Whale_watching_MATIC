from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum
from pydantic import BaseModel

from AllTokenMoralis import allToken,proportion,pieChart
from MaticTransactions import historicalBalanceValue

app = FastAPI()

origins = [
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/list")
async def root():
    return allToken('0x4e65175f05b4140a0747c29cce997cd4bb7190d4')


@app.get("/bigchart")
async def root():
     return pieChart()

@app.get("/historicalTx")
async def root():
    return historicalBalanceValue("0x87504c734b79127df3397fcbf38ec15080ead4e0")