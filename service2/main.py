from .app import app
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
    transactions = await transactions()
    return [services, users, transactions]

###############
# Main function
###############
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
