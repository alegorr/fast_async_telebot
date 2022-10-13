from app import app
from fastapi import Request
from tb import pull_messages, TELEBOT_API_TOKEN

@app.post(TELEBOT_API_TOKEN + "/")
async def telebot_pull_messages(request: Request):
    await pull_messages(request)

###############
# Main function
###############
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
