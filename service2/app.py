from fastapi import FastAPI
from .tb import TELEBOT_NAME, telebot_init, telebot_stop
from .db import db

##########
# Init app
##########
app = FastAPI(title="Async FastAPI Telebot {}".format(TELEBOT_NAME))

@app.on_event("startup")
async def startup():
    await db.connect()
    await telebot_init()

@app.on_event("shutdown")
async def shutdown():
    await telebot_stop()
    await db.disconnect()
