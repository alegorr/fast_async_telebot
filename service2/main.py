from .app import app
from .tb import TELEBOT_API_TOKEN, pull_messages
from .api import services_list, users_list, transactions_list

#############
# API methods
#############
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

@app.get("/all/")
async def get_all():
    services = await services_list()
    users = await users_list()
    transactions = await transactions_list()
    return [services, users, transactions]

##############
# Webhook cast
##############
@app.post("/{}/".format(TELEBOT_API_TOKEN), status_code=200)
async def telebot_pull_messages(request: Request):
    print("Pull messages fired!")
    #await pull_messages(request)
    return "OK"

###############
# Main function
###############
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
