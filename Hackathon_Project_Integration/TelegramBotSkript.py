#import of all needed packages
import json
import requests
import time
import urllib
#import logging

#token and url for telegram access
TOKEN = "386823692:AAFGIZvCUw7AVXIhxLICHIjeLNetgeO3mfw"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

#declaration of variables for Bot authorization and notification handling
#global professors, students, break_requests
professors = [264043624]
students = []
break_requests = []
#164399314

class TelegramBot:
    def __init__(self):
        pass

    #returns content of a url response
    def get_url(self, url):
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content

    #formats url response as json
    def get_json_from_url(self, url):
        content = TelegramBot.get_url(self, url)
        js = json.loads(content)
        return js

    #gets updates from telegram every 10 seconds
    def get_updates(self, offset=None):
        url = URL + "getUpdates?timeout=10"
        if offset:
            url += "&offset={}".format(offset)
        js = TelegramBot.get_json_from_url(self, url)
        return js

    #returns the id of the last update received from telegram
    def get_last_update_id(self, updates):
        update_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)

    #registers a new student by appending their user id to the students list
    #student will now receive notifications and be able to request a break
    def register(self, user_id):
        global students
        students.append(user_id)

    #unregisters a specific student by removing their user id from the students list
    #student will no longer receive notifications and be able to request a break
    def unregister(self, user_id):
        global students
        students.remove(user_id)

    #send a telegram message to a specific chat id
    def send_message(self, text, chat_id, reply_markup=None):
        text = urllib.parse.quote_plus(text)
        url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
        if reply_markup:
            url += "&reply_markup={}".format(reply_markup)
        TelegramBot.get_url(self, url)

    #sends a telegram message to all user ids currently registered as professor or student
    def send_message_to_all(self, text, reply_markup=None):
        global professors, students
        chat_ids = professors + students
        for i in chat_ids:
            TelegramBot.send_message(self, text, i)
            

    #builds a custom inline keyboard
    #idea was to enable break requests via a button as well as the /break command in telegram
    #not yet fully implemented
    def build_keyboard(self):
        keyboard = ['breakrequest']
        reply_markup = {"keyboard":keyboard, "one_time_keyboard": False}
        return json.dumps(reply_markup)

    #handle updates received by the telegram bot
    def handle_updates(self, updates):
        global professors, students, break_requests
        for update in updates["result"]:
            try:
                #extract the input text, chat id and user id from the telegram update
                text = update["message"]["text"]
                chat = update["message"]["chat"]["id"]
                user = update["message"]["from"]["id"]
                chat_ids = professors + students
                #handle break requests
                if text == "/break":
                    #users that have previously requested a break cannot do so again
                    if user in break_requests:
                        TelegramBot.send_message(self, "already requested break earlier", chat)
                        #logger.info("A user tried to request a break. Request was denied due to existing request.")
                    #users have to be registered (either as a student or a professor) to request a break
                    elif user in chat_ids:
                        info = {"entity_id": "input_boolean.breakrequest"}
                        #toggle_button(self, info) #XXX - muss noch gemacht werden
                        TelegramBot.send_message(self, "break requested", chat)
                        break_requests.append(user)
                        #logger.info("A user requested a break.")
                    #unknown users are asked to register before they can request a break
                    else:
                        TelegramBot.send_message(self, "please register as a student via /register in order to be able to request a break", chat)
                        #logger.info("A user tried to request a break. Request was denied due to missing student status.")
                #handle lecture start request
                elif text == "/start_lecture":
                    #user needs to be a professor in order to successfully start the lecture
                    if user in professors:
                        value = {"attributes": {"friendly_name": "Lecture"}, "state": "on"}
                        #set_state(self, "input_boolean.stopwatch", value) # XXX - muss noch gemacht werden
                        #send_message_to_all("the lecture has started")
                        #logger.info("A professor started the lecture.")
                    else:
                        TelegramBot.send_message(self, "only professors are allowed to use this function", chat)
                        #logger.info("A student tried to start the lecture. Request was denied.")
                #handle lecture stop request
                elif text == "/stop_lecture":
                    #user needs to be a professor in order to successfully stop the lecture
                    if user in professors:
                        value = {"attributes": {"friendly_name": "Lecture"}, "state": "off"}
                        #set_state(self, "input_boolean.stopwatch", value) # XXX - muss noch gemacht werden
                        break_requests.clear()
                        al1 = 0
                        al2 = 0
                        al3 = 0
                        #send_message_to_all("the lecture has stopped")
                        #logger.info("A professor stopped the lecture.")
                    else:
                        TelegramBot.send_message(self, "only professors are allowed to use this function", chat)
                        #logger.info("A student tried to stop the lecture. Request was denied.")
                #handle request to register as a student
                elif text == "/register":
                    #a user can only be register as a student once (unless they unregistered in the meantime)
                    if user in students:
                        TelegramBot.send_message(self, "you are already registered as a student", chat)
                        #logger.info("A student tried to register a second time. Request was denied.")
                    #professors cannot register as a student
                    elif user in professors:
                        TelegramBot.send_message(self, "you are already registered as a professor", chat)
                        #logger.info("A professor tried to register as a student. Request was denied.")
                    #if a user is neither previously registered as a student or professor, they are added as a student
                    else:
                        TelegramBot.send_message(self, "you are now registered as a student", chat)
                        #logger.info("A new student registered.")
                        TelegramBot.register(self, user)
                #handle request to unregister as a student
                elif text == "/unregister":
                    #a user registered as a student will be removed from the student list
                    if user in students:
                        TelegramBot.unregister(self, user)
                        TelegramBot.send_message(self, "you are no longer registered as a student. you will not receive further notifications", chat)
                        #logger.info("A student unregistered.")
                    #professors cannot unregister via this function
                    elif user in professors:
                        TelegramBot.send_message(self, "you are registered as a professor. you cannot unregister via this button", chat)
                        #logger.info("A professor tried to unregister as a student. Request was denied.")
                    #anyone not in the student list cannot unregister from student status
                    else:
                        TelegramBot.send_message(self, "you were not registered in the first place", chat)
                        #logger.info("Someone not registered tried to unregister. Request was denied.")
                #handle info that button was toggled in home assistant
                elif text == "lectureStop":
                    TelegramBot.send_message_to_all(self, "the lecture was ended")
                    #logger.info("the lecture button was ended")
                elif text == "lectureStart":
                    TelegramBot.send_message_to_all(self, "the lecture was started")
                    #logger.info("the lecture button was started")
                #handle alert that breakscore has exceeded limit, send message to users
                elif text == "breakAlert":
                    TelegramBot.send_message_to_all(self, "you should take a break. conditions in the room are no longer optimal.")
                    #logger.info("alert to take break sent.")
                #handle alert that temperature too low, send message to users
                elif text == "tempTooLow":
                    TelegramBot.send_message_to_all(self, "you should turn on the heating. it is too cold in the room.")
                    #logger.info("alert: temperature too low.")
                #handle alert that temperature too high, send message to users
                elif text == "tempTooHigh":
                    TelegramBot.send_message_to_all(self, "you should turn on the air conditioning. it is too hot.")
                    #logger.info("alert: temperature too high.")
                #handle alert that humidity is too dim, send message to users
                elif text == "humTooLow":
                    TelegramBot.send_message_to_all(self, "it is not humid enough in the room.")
                    #logger.info("alert: humidity too low.")
                #handle alert that humidity is too high, send message to users
                elif text == "humTooHigh":
                    TelegramBot.send_message_to_all(self, "it is too humid.")
                    #logger.info("alert: humidity too high.")
                #handle alert that Co2 value is too high, send message to users
                elif text == "Co2TooHigh":
                    TelegramBot.send_message_to_all(self, "you should open a window. the air quality has gotten too bad.")
                    #logger.info("alert: Co2 too high.")
                #handle alert that brightness is too low, send message to users
                elif text == "lightTooLow":
                    TelegramBot.send_message_to_all(self, "it is too dark in the room. consider turning on the lights.")
                    #logger.info("alert: brightness too low.")
                #handle input not recognized as one of the above cases
                else:
                    TelegramBot.send_message(self, "invalid input. please use one of the commands found under /", chat)
                    #logger.info("Invalid input.")
            #catch exceptions - avoid script disruption due to temporary unavailability of home assistant (such as reboot)
            except Exception as e:
                    print(e)
