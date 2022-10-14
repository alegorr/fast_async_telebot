from .schema import ServiceSchema
from .models import User, Service, Transaction
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Update
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

TELEBOT_API_TOKEN = str(os.environ["TELEBOT_API_TOKEN"])

##########
# Init bot
##########
bot = AsyncTeleBot(TELEBOT_API_TOKEN)

async def telebot_init():
    # set webhook
    TELEBOT_WEBHOOK_URL = 'https://%s/%s/' % (os.environ["TELEBOT_WEBHOOK_HOST"], os.environ["TELEBOT_API_TOKEN"])
    try:
        await bot.remove_webhook()
    except:
        pass
    try:
        await bot.set_webhook(url=TELEBOT_WEBHOOK_URL)
    except Exception as err:
        print("Can not set Telebot webhook: ", err)
    # add services
    TELEBOT_KNOWN_SERVICES = []
    try:
        TELEBOT_KNOWN_SERVICES = zip(os.environ['TELEBOT_KNOWN_SERVICES'].split(","), os.environ['TELEBOT_KNOWN_SERVICES_NAMES'].split(","))
        for service_url, service_name in TELEBOT_KNOWN_SERVICES:
            try:
                service_id = await Service.create(service_name, service_url)
                if service_id:
                    print("add service ", service_url)
                else:
                    print("service already added")
            except Exception as err:
                print("add service error ", err)
    except Exception as err:
        print("no services added ", err)

async def telebot_stop():
    await bot.close_session()

##################
# Helper functions
##################
async def get_user(message):
    u = message.from_user
    uid = None
    try:
        uid = await User.get(u.id)
        if uid is None:
            user_data = {
                "id": u.id,
                "is_bot": u.is_bot,
                "username": u.username,
                "service_id": 0
            }
            uid = await User.create(**user_data)
    except Exception as err:
        print("get user error ", err)
    return uid

async def get_service(service_name):
    sid = None
    try:
        sid = await Service.get(service_name)
    except Exception as err:
        print(err)
    return sid

async def services_list():
    try:
        services_lst = await Service.get_all()
        services = list()
        for s in services_lst:
            services.append(ServiceSchema(**s))
        print(services)
        return services
    except Exception as err:
        print(err)
        return list()

async def get_help_message():
    services_info = ""
    try:
        services = await services_list()
        for service in services:
            services_info += service.name + "\n"
    except:
        services_info = "None"
    return messages.BOT_HELP_MESSAGE + services_info

async def set_user_service(uid, sid, service_name):
    if uid and sid:
        try:
            await User.set_service(uid, sid)
            await bot.send_message(message.chat.id, text=messages.BOT_SERVICE_MESSAGE.format(service_name))
        except Exception as err:
            print("can not set user service ", err)

async def make_transaction(message):
    try:
        uid = await get_user(message)
        sid = await User.get_service(uid)
        transaction_data = {
            "user_id": uid,
            "service_id": service_id,
            "input": input_text,
            "output": "",
            "complete": false,
            "error": ""
        }
        tid = create_transaction(transaction_data)
        async with httpx.AsyncClient() as client:
            print("sending message ", message.text)
            result = await client.post(service_address, data={"sentences": message.text.split(",")})
            if result.status_code == 200:
                text = str(result.json())
                await Transaction.update(tid, {"output": text})
                print("transaction succeeded +", tid)
                await bot.send_message(chat_id=message.chat.id, text=text)
                await Transaction.update(tid, {"complete": True})
                print("transaction complete ", tid)
            else:
                err_msg = messages.BOT_ERROR_MESSAGE % str(result.status_code)
                await bot.send_message(chat_id=message.chat.id, text=err_msg)
                await Transaction.update(tid, {"error": str(result.status_code)})
                print("transaction error {}".format(result.status_code), tid)
    except Exception as err:
        print("error process message: ", err)


##################
# Message handlers
##################
@bot.message_handler(commands=['start'])
async def show_start_message(message):
    await bot.send_message(message.chat.id, text=messages.BOT_START_MESSAGE)

@bot.message_handler(commands=['help'])
async def show_help(message):
    help_message = await get_help_message()
    await bot.send_message(message.chat.id, text=help_message)

@bot.message_handler(commands=['bad'])
async def choose_bad_service(message):
    await set_user_service(get_user(message), get_service('badlisted_words'), 'badlisted_words')

@bot.message_handler(commands=['spacy'])
async def choose_spacy_service(message):
    await set_user_service(get_user(message), get_service('spacy_nounphrases'), 'spacy_nounphrases')

@bot.message_handler(func=lambda message: message.text not in messages.BOT_KNOWN_COMMANDS, content_types=['text'])
async def process_message(message):
    await make_transaction(message)

#######################
# Process webhook calls
#######################
async def pull_messages(request):
    print(request.body().decode("utf-8"))
    updates = Update.de_json(request.body().decode("utf-8"))
    await bot.process_new_updates([updates])
