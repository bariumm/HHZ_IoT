#import of all needed packages
import json
#import requests
import time
#import urllib
#import logging
import homeassistant.remote as remote
import configparser
import ast
from TelegramBotSkript import TelegramBot
from farbenfroh import FarbenFroh


al1 = 0
al2 = 0
al3 = 0
fake_update = {'ok': True, 'result': [{'update_id': 0, 'message': {'message_id': 765, 'from': {'id': 0, 'first_name': 'J', 'language_code': 'de-DE'}, 'text': '', 'chat': {'type': 'private', 'id': 0, 'first_name': 'J'}, 'date': 1497357549, 'entities': [{'offset': 0, 'type': 'bot_command', 'length': 6}]}}]}

#Config
Config = configparser.ConfigParser()
Config.read("config.ini")
#logging.basicConfig(format='%(asctime)s;%(message)s', datefmt='%Y.%m.%d;%H:%M:%S', level=logging.INFO, filename='sensor.csv')

#Connect to Home Assistant
api = remote.API(Config.get('HomeAssistant', 'IP'), Config.get('HomeAssistant', 'PW'))

#Create lists for sensor IDs
temperature_ids = []
co2_ids = []
humidity_ids = []
light_ids = []

#Global Variable
goodRoom = True

#Get relevant sensor IDs from Home Assistant
entities = remote.get_states(api)
#print(entities) # XXX - entities angucken, um zu sehen, wie timer und request counter heißen
for entity in entities:
    if str(entity).__contains__(Config.get('Sensors', 'Room')) and not str(entity).__contains__("group"):
        if str(entity).__contains__("temp"):
            temperature_ids.append(entity.entity_id)
        elif str(entity).__contains__("co2"):
            co2_ids.append(entity.entity_id)
        elif str(entity).__contains__("hum"):
            humidity_ids.append(entity.entity_id)
        elif str(entity).__contains__("light"):
            light_ids.append(entity.entity_id)
        #XXX - add motion?
            
#Default values
values = {'temp_min': False, 'temp_max': False, 'temp_bright': 0, 'hum_min': False, 'hum_max': False, 'hum_bright': 0, 'Co2_max': False, 'Co2_bright': 0, 'light_min': False}
tempAvg = 22
humAvg = 50
Co2Avg = 300
lightAvg = 600

farbenFroh = FarbenFroh()
telegramBot = TelegramBot()

#logger setup
#logger = logging.getLogger('myapp')
#hdlr = logging.FileHandler('/home/homeassistant/.homeassistant/logs/TelegramBot.log')
#formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#hdlr.setFormatter(formatter)
#logger.addHandler(hdlr)
#logger.setLevel(logging.INFO)

def checkHAStatus():
    #check if lecture status has changed, send update to telegram bot so it can react accordingly
    value = remote.get_state(api, XXX) #replace by ID of lecture button - evtl oben id wie bei sensoren setzen(!)
    if response['state'] == response1:
        pass
    else:
        if response['state'] == "on":
            return 'lectureStop'
            break_requests.clear()
            al1 = 0
        else:
            return 'lectureStart'
        response1 = response['state']
    #check if break score has exceeded limit, send update to telegram bot so it can notify users
    value = remote.get_state(api, XXX) #replace by ID of break score - evtl oben id wie bei sensoren setzen(!)
    if response['state'] < 100:
        pass
    else:
        if al1 == 0:
            al1 = 1
            return 'breakAlert'
        else:
            pass

#main function - contains an infinite loop
#gets all new updates from telegram since the last update processed by this script
#calls the function handle updates to react to telegram updates
#then handles any possible status changes in home assistant (lecture turned on/off, limits for break/air quality/brightness crossed)
def main():
    global tempAvg, humAvg, Co2Avg, lightAvg, fake_update
    last_update_id = None
    response1 = None
    #keyboard = build_keyboard()
    while True:
        print('started loop')
        try:
            tempAvg = farbenFroh.getStateAvg(api, temperature_ids)
            humAvg = farbenFroh.getStateAvg(api, humidity_ids)
            Co2Avg = farbenFroh.getStateAvg(api, co2_ids)
            lightAvg = farbenFroh.getStateAvg(api, light_ids)
            print(tempAvg, humAvg, Co2Avg, lightAvg)
        except Exception as e:
            print("Getting states: "+str(e))
            pass
        try:
            updates = telegramBot.get_updates(last_update_id)
            if len(updates["result"]) > 0:
                last_update_id = telegramBot.get_last_update_id(updates) + 1
                telegramBot.handle_updates(updates)
                time.sleep(1)
        except Exception as e:
            print("Telegram Msgs: "+str(e))
            pass
        try:
            text = farbenFroh.changeLightColor(Config, values, tempAvg, humAvg, Co2Avg, lightAvg)
            fake_update['result']['message']['text'] = text
            telegramBot.handle_updates(fake_update)
        except Exception as e:
            print("Change Color: "+str(e))
            pass
        try:
            text = checkHAStatus()
            fake_update['result']['message']['text'] = text
            telegramBot.handle_updates(fake_update)
        except Exception as e:
            print("Send status to TG: "+str(e))
            pass

#executes main function upon start of python script
if __name__ == '__main__':
        main()
        
        
#toggles the button in the home assistant interface
#used to request breaks and turn lecture on and off
def toggle_button(info): # XXX - muss evtl in Telegram Skript, da dort aufgerufen, braucht dann aber HA imports
    r = requests.post("http://192.168.1.135:8123/api/services/input_boolean/toggle", json=info)
    #remote.call_service(api, 'switch', 'turn_on', {'entity_id': '{}'.format('switch.XXX')}) #replace by name of lecture button
    #remote.call_service(api, 'switch', 'turn_off', {'entity_id': '{}'.format('switch.XXX')}) #replace by name of lecture button


#set state of an entity via Python API
#import homeassistant.remote as remote
#from homeassistant.const import STATE_ON
#api = remote.API('127.0.0.1', 'YOUR_PASSWORD')
#remote.set_state(api, 'sensor.office_temperature', new_state=123)
#remote.set_state(api, 'switch.livingroom_pin_2', new_state=STATE_ON)