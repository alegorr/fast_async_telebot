from telebot.async_telebot import AsyncTeleBot
from telebot.types import Update
from .models import User, Service, Transaction
from .messages import *
import httpx
from dotenv import load_dotenv
import os

############
# Setup vars
############
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

TELEBOT_NAME = str(os.environ["TELEBOT_NAME"])
TELEBOT_API_TOKEN = str(os.environ["TELEBOT_API_TOKEN"])
TELEBOT_KNOWN_SERVICES = zip(os.environ['TELEBOT_KNOWN_SERVICES_NAMES'].split(","), os.environ['TELEBOT_KNOWN_SERVICES_URLS'].split(","))

TELEBOT_WEBHOOK_HOST = str(os.environ["TELEBOT_WEBHOOK_HOST"])
TELEBOT_WEBHOOK_PORT = str(os.environ["TELEBOT_WEBHOOK_PORT"])
TELEBOT_WEBHOOK_URL = 'https://%s:%s/%s/' % (TELEBOT_WEBHOOK_HOST, TELEBOT_WEBHOOK_PORT, TELEBOT_API_TOKEN)

TELEBOT_WEBHOOK_CERT = str(os.environ["TELEBOT_WEBHOOK_CERT"])
TELEBOT_WEBHOOK_KEY = str(os.environ["TELEBOT_WEBHOOK_KEY"])

################
# Init async bot
################
bot = AsyncTeleBot(TELEBOT_API_TOKEN)

async def telebot_init():
    print("{} bot init...".format(TELEBOT_NAME))
    # set webhook
    print('Telebot webhook url: ', TELEBOT_WEBHOOK_URL)
    try:
        print("remove old webhook...")
        await bot.remove_webhook()
        print("remove old webhook... Done.")
    except:
        pass
    try:
       print("set Telebot webhook...")
       await bot.set_webhook(url=TELEBOT_WEBHOOK_URL, certificate=open(TELEBOT_WEBHOOK_CERT, 'r'))
       print("set Telebot webhook... Done.")
       print("get webhook info...")
       webhook_info = await bot.get_webhook_info()
       print('webhook info ', webhook_info)
    except Exception as err:
       print("Can not set Telebot webhook: ", err)
    #
    print("Register services...")
    try:
        for service_name, service_url in TELEBOT_KNOWN_SERVICES:
            try:
                service_id = await Service.create(service_name, service_url)
                print("service {} () registered".format(service_name, service_url))
            except Exception as err:
                print("registering service error ", err)
    except Exception as err:
        print("registering service error: no services added ", err)
    print("Start bot messaging...")
    await bot.polling()
    print("Ok!")

async def telebot_stop():
    print("Stop bot messaging...")
    await bot.close_session()
    print("Bot stop messaging.")

##################
# Helper functions
##################
async def get_user(message):
    u = message.from_user
    user = None
    try:
        print("Try to get user {}".format(u.id))
        user = await User.get(u.id)
        print("user is registered") if user else print("user is not registered")
        if user is None:
            print("Register new user...")
            first_service = await Service.get_first_service()
            print("set user {} service (by default) ".format(first_service.name))
            user_data = {
                "id": u.id,
                "is_bot": u.is_bot,
                "username": u.username,
                "service_id": first_service.id
            }
            uid = await User.create(**user_data)
            user = await User.get(uid)
            print("user {} successfully registered.".format(user.username))
    except Exception as err:
        print("get user error ", err)
    return user

async def get_service(service_name):
    service = None
    try:
        service = await Service.get_by_name(service_name)
    except Exception as err:
        print("can not get service ", err)
    return service

async def get_help_message():
    services_info = ""
    try:
        services = await Service.get_all()
        for service in services:
            services_info += service.name + "\n"
    except:
        services_info = "None"
    return BOT_HELP_MESSAGE + services_info

async def set_user_service(message, service_name):
    print("Set user service ", service_name)
    user = await get_user(message)
    service = await get_service(service_name)
    if user and service:
        try:
            await User.set_service(user.id, service.id)
            print("service {} succesfully seted to user {}".format(service.name, user.name))
            await bot.reply_to(message, text=BOT_SERVICE_MESSAGE.format(service_name))
        except Exception as err:
            print("can not set user service ", err)
    else:
        print("can't find such user or service ")

async def make_transaction(message):
    try:
        print("Trying to make a transaction...")
        user = await get_user(message)
        service = await User.get_service(user.service_id)
        transaction_data = {
            "user_id": user.id,
            "service_id": service.id,
            "input": message.text,
            "output": "",
            "complete": False,
            "error": ""
        }
        tid = await Transaction.create(**transaction_data)
        print("Transaction created ", tid)
        async with httpx.AsyncClient() as client:
            print("Transaction: sending message...\n>>>")
            print(message.text)
            print(">>>")
            result = await client.post(service.address, data={"sentences": message.text.split(",")})
            if result.status_code == 200:
                text = str(result.json())
                print("Transaction: data received\n>>>")
                print(text)
                print(">>>")
                print("Transaction: update...")
                await Transaction.update(tid, {"output": text})
                print("Transaction: update succeeded +", tid)
                print("Transaction: send bot message...")
                await bot.reply_to(message, text=text)
                print("Transaction: send bot message... Ok!")
                await Transaction.update(tid, {"complete": True})
                print("Transaction: complete ", tid)
            else:
                print("Transaction: data lost")
                print("Transaction: status code ", result.status_code)
                err_msg = BOT_ERROR_MESSAGE % str(result.status_code)
                print("Transaction: sending error bot message...")
                await bot.reply_to(message, text=err_msg)
                print("Transaction: sending error bot message... Ok!")
                await Transaction.update(tid, {"error": str(result.status_code)})
                print("Transaction: error {}".format(result.status_code), tid)
    except Exception as err:
        print("Transaction get error ", err)

##################
# Message handlers
##################
@bot.message_handler(commands=['start'])
async def show_start_message(message):
    await bot.reply_to(message, text=BOT_START_MESSAGE)

@bot.message_handler(commands=['help'])
async def show_help(message):
    help_message = await get_help_message()
    await bot.reply_to(message, text=help_message)

@bot.message_handler(commands=['bad'])
async def choose_bad_service(message):
    await set_user_service(message, 'badlisted_words')

@bot.message_handler(commands=['spacy'])
async def choose_spacy_service(message):
    await set_user_service(message, 'spacy_nounphrases')

@bot.message_handler(func=lambda message: message.text not in BOT_KNOWN_COMMANDS, content_types=['text'])
async def process_message(message):
    await make_transaction(message)

#######################
# Process webhook calls
#######################
async def pull_messages(request):
    try:
        print("Pull messages start...")
        request_body = await request.body()
        print(request_body)
        data = request_body.decode("utf-8")
        updates = Update.de_json(data)
        print(updates)
        print("process updates...")
        await bot.process_new_updates([updates])
        print("updates processed.")
    except Exception as err:
        print("Can't process new updates ", err)
