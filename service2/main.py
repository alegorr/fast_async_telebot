from .app import app
from fastapi import Request
from .tb import pull_messages, TELEBOT_API_TOKEN
from .api import services_list, users_list, transactions_list

TELEBOT_API_ROUTE = "/{}/".format(TELEBOT_API_TOKEN)
@app.post(TELEBOT_API_ROUTE, status_code=200)
async def telebot_pull_messages(request: Request):
    print("Pull messages fired!")
    #await pull_messages(request)
    return "OK"

@app.get("/services/")
async def get_services():
    services = await services_list()
    return services

@app.get("/users/")
async def get_users():
    users = await users_list()
    return users

@app.get("/transactions/")
async def get_transactions():
    transactions = await transactions_list()
    return transactions

###############
# Main function
###############
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
