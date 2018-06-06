
import logging
import settings
from bot import Bot
from mongodb import Database
import pprint

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=settings.LOGLEVEL)

bot = Bot(token=settings.TOKEN)
db = Database()

@bot.on_message
def on_message(bot, update):
  user = db.getUser(update.message.from_user.id)

  # print(user)
  # print(update.message.from_user) # user information such as name and id

  if(not user):
    handle_newUser(bot, update)
    return

  if(user.state == "asking"):
    handle_question(bot, update)
  if(user.state == "answering"):
    handle_answer(bot, update)
  if(user.state == "modeling"):
    handle_model(bot, update)
  if(user.state == "idle"):
    handle_idle(bot, update)

# Figure out new state here
def handle_idle(bot, update):
  echo(bot, update)

# Figure out crowdsource task here
def handle_question(bot, update):
  echo(bot, update)

# Figure out answer to question here
def handle_answer(bot, update):
  echo(bot, update)

# Handle user model here
def handle_model(bot, update):
  echo(bot, update)

def handle_newUser(bot, update):
  db.createUser(update.message.from_user.id, update.message.from_user.first_name)

# placeholder
def echo(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Hi " + user.username)

@bot.command('start')
def start(bot, update):
  if(not db.getUser(update.message.from_user.id)):
    handle_newUser(bot, update)
  
  bot.send_message(chat_id=update.message.chat_id, text="Hi " + update.message.from_user.first_name)


bot.start_polling()