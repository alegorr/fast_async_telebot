from fastapi import FastAPI
from .db import db
from .tb import telebot_init, telebot_stop

app = FastAPI(title="Async FastAPI Telebot")

@app.on_event("startup")
async def startup():
    await db.connect()
    await telebot_init()


@app.on_event("shutdown")
async def shutdown():
    await telebot_stop()
    await db.disconnect()
