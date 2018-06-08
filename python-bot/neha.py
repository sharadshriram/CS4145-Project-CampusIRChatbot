import requests
import datetime
import numpy as np
import pandas as pd
import numpy as np
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

class BotHandler:
    def _init_(self, token):
            self.token = token
            self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=0, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_first_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[0]
        else:
            last_update = None

        return last_update


token = '372773930:AAEs3XKL8kMolM79widGhEWNGzzqKTLTIXQ'
myci_bot = BotHandler(token)


def main():
    new_offset = 0
    print('Launching MyCI...')
    while True:
        all_updates=myci_bot.get_updates(new_offset)
        columns = ['user_id','first_name', 'C1','C2']
        users = pd.DataFrame(columns=columns)
        users_with_yes = users
        users_with_no = users
        users_without = users
        if len(all_updates) > 0:
            for current_update in all_updates:
                first_update_id = current_update['update_id']
                if 'text' not in current_update['message']:
                    first_chat_text='New member'
                else:
                    first_chat_text = current_update['message']['text']
                first_chat_id = current_update['message']['chat']['id']
                if 'first_name' in current_update['message']:
                    first_chat_name = current_update['message']['chat']['first_name']
                elif 'new_chat_member' in current_update['message']:
                    first_chat_name = current_update['message']['new_chat_member']['username']
                elif 'from' in current_update['message']:
                    first_chat_name = current_update['message']['from']['first_name']
                else:
                    first_chat_name = "unknown"

                if first_chat_id not in users['user_id']:
                    users = users.append(pd.DataFrame(np.array([first_chat_id, first_chat_name, 0, 0]).reshape(1,4),columns=columns))
                    users[['C1']]=users[['C1']].apply(pd.to_numeric)
                    users[['C2']]=users[['C2']].apply(pd.to_numeric)

                first_chat_text = first_chat_text.lower()
                if first_chat_text == '/start':
                    myci_bot.send_message(first_chat_id, 'Welcome ' + first_chat_name+
                                                          '\n Type /question to ask a question')
                    new_offset = first_update_id + 1
                elif first_chat_text == 'hi' or first_chat_text == 'hello':
                    myci_bot.send_message(first_chat_id, 'Hi! How can I help you '+first_chat_name+'?'+
                                                             '\n Type /question to ask a question')
                    new_offset = first_update_id + 1
                elif first_chat_text == '/question':
                    #addmore functionalities if needed in future
                    # may be finding team mates for projects etc.
                    myci_bot.send_message(first_chat_id, 'Type /recommendation if you need course recommendation')
                    new_offset = first_update_id + 1
                elif first_chat_text == '/recommendation':
                    #addmore functionalities if needed in future
                    # may be finding team mates for projects etc.
                    myci_bot.send_message(first_chat_id, 'Type in the course name')
                    new_offset = first_update_id + 1
                elif first_chat_text == 'c1':
                    #display full course name
                        users_with_yes = users['user_id'][users['C1']==1]
                        users_with_no = users['user_id'][users['C1']==-1]
                        users_without = users['user_id'][users['C1']==0]
                        myci_bot.send_message(first_chat_id, first_chat_name+' We will get back to you when we have the recommendations')
                        new_offset = first_update_id + 1
                elif first_chat_text == 'c2':
                    #display full course name
                        users_with_yes = users['user_id'][users['C2']==1]
                        users_with_no = users['user_id'][users['C2']==-1]
                        users_without = users['user_id'][users['C2']==0]
                        myci_bot.send_message(first_chat_id, first_chat_name+' We will get back to you when we have the recommendations')
                        new_offset = first_update_id + 1
                else:
                    myci_bot.send_message(first_chat_id, 'There was some error. Can you please try again '+first_chat_name+'?')
                    new_offset = first_update_id + 1

                #store this user_id(the one who asked question) and the corresponding course name in a separate database
                #create this for each task and drop when it is done and update info in original database
                #sending questions to workers
                #yes
                if len(users_with_no)>0:
                    myci_bot.send_message(users_with_no, 'Do you have any idea about c1 ?')
                if len(users_with_yes)>0:
                    myci_bot.send_message(users_with_yes, 'There was some error. Can you please try again '+first_chat_name+'?')
                if len(users_without)>0:
                    myci_bot.send_message(users_without, 'Can you give a suggestion ?')

if _name_ == '_main_':
    try:
        main()
    except KeyboardInterrupt:
        exit()