from schema import UserSchema, ServiceSchema, TransactionSchema
from models import User, Service, Transaction
from typing import List
from app import app
from db import db

@app.post("/create/user/")
async def create_user(user: UserSchema):
    try:
        uid = await User.create(**user.dict())
        return uid
    except Exception as err:
        return err

@app.get("/get/user/{id}")
async def get_user(id: int):
    try:
        user = await User.get(id)
        if user:
            return UserSchema(**user).dict()
        else:
            return  {"msg": "no content"}
    except Exception as err:
        print(err)
        return {"err":str(err)}

@app.post("/create/service/")
async def create_service(service: ServiceSchema):
    try:
        sid = await Service.create(**service.dict())
        return sid
    except Exception as err:
        print(err)
        return {"err":str(err)}

@app.get("/get/service/{id}")
async def get_service(id: int):
    try:
        service = await Service.get(id)
        return ServiceSchema(**service).dict()
    except Exception as err:
        print(err)
        return {"err":str(err)}

@app.post("/create/transaction/")
async def create_transaction(transaction: TransactionSchema):
    try:
        tid = await Transaction.create(**transaction.dict())
        return tid
    except Exception as err:
        print(err)
        return {"err":str(err)}

@app.get("/get/transaction/{id}")
async def get_transaction(id: int):
    try:
        transaction = await Transaction.get(id)
        return TransactionSchema(**transaction).dict()
    except Exception as err:
        print(err)
        return {"err":str(err)}

@app.get("/", response_model=List[TransactionSchema])
async def transactions_list():
    try:
        transactions_list = await Transaction.get_all()
        resp = list()
        for t in transactions_list:
            resp.append(TransactionSchema(**t).dict())
        return resp
    except Exception as err:
        print(err)
        return list()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
