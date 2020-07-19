# based on code from: https://github.com/sixhobbits/python-telegram-tutorial
import json
import requests
import time
import urllib
import datetime
import os


def get_my_dir():
    return os.path.split(os.path.abspath(__file__))[0]

token = open(get_my_dir() +"/token").read().strip()
id = open(get_my_dir() +"/id").read().strip()
try:
    user = open(get_my_dir() +"/user").read().strip()
except:
    user = None
URL = "https://api.telegram.org/bot"+ token +"/"

def log_data(key, val):
    timeStamp =datetime.datetime.strftime(datetime.datetime.now(), "%d%b%Y_%H:%M.%S")
    data_file = get_my_dir() +"/data.yaml"
    data = "- {timeStamp: '"+ timeStamp +"', '"+ key +"':'"+ str(val) +"'}"
    open(data_file, 'a').write(data +"\n")


def toLog(msg):
    timeStamp =datetime.datetime.strftime(datetime.datetime.now(), "%d%b_%H:%M.%S")
    try:
        width = os.get_terminal_size()[0]
    except:
        width = None
    if width:
        toScreen = timeStamp +" "+ msg
        if len(toScreen)>width-1:
            toScreen = toScreen[:width-5] +"..."
        print(toScreen)
    log_file = get_my_dir() +"/moodTrackBot.log"
    open(log_file, 'a').write(timeStamp +" "+ msg +"\n")
    
def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        send_message(text, chat)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

#button_list = []
#button_list.append(telegram.InlineKeyboardButton('Button One', callback_data='query_one'))
#button_list.append(telegram.InlineKeyboardButton('Button two', callback_data='query_two'))
#rmu = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=2))

def send_question(question, keyword):
    send_message( question, id, build_keyboard([keyword+"-"+str(i) for i in range(1,11)]) )


# Everything in the updates before we send the first message is not interesting (stale)

not_yet_handled_update_id = None
updates = get_updates()
if len(updates["result"]) > 0:
    toLog("Got updates before sending first question - will be ignored")
    toLog("Documenting stale updates:")
    for result in updates["result"]:
        toLog("    Stale result: "+ str(result))
    not_yet_handled_update_id = get_last_update_id(updates) + 1

toLog("    Before sending intial msg")
send_question( 'What is your energy ?', "energy")
toLog("    After sending intial msg")

done = False
while not done:
    updates = get_updates(not_yet_handled_update_id)
    if len(updates["result"]) > 0:
        not_yet_handled_update_id = get_last_update_id(updates)+1
        toLog("")
        toLog("Got new updates")
        for result in updates["result"]:
            toLog("-------------------------------------------")
            toLog("    Current result: "+ str(result))
            reply = result["message"]["text"]
            if "reply_to_message" in result["message"].keys():
                reply_to_message = result["message"]["reply_to_message"]["text"]
            else:
                reply_to_message = ""
            toLog("    "+ reply_to_message +" --> "+ reply)
            #if reply_to_message=='What is your energy ?':
            if reply.startswith("energy-") and reply[len("energy-"):].isdigit():
                log_data("Energy", reply.split("-")[-1])
                send_question( 'What is your mood ?', "mood")
            #elif reply_to_message=='What is your mood ?':
            elif reply.startswith("mood-") and reply[len("mood-"):].isdigit():
                log_data("Mood", reply.split("-")[-1])
                send_question( 'How much did you do today ?', "howMuch")
            #elif reply_to_message=='How much did you do today ?':
            elif reply.startswith("howMuch-") and reply[len("howMuch-"):].isdigit():
                log_data("Done-today", reply.split("-")[-1])
                done = True
            else:
                toLog("Got unknown text in result - it is Ok - just ignoring it")
        time.sleep(0.5)

