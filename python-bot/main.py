
import logging
import settings
from bot import Bot
from mongodb import Database
import pprint

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=settings.LOGLEVEL)

bot = Bot(token=settings.TOKEN)
db = Database()

@bot.command('start')
def start(bot, update):
  if(not db.getUser(update.message.from_user.id)):
    db.createUser(update.message.from_user.id, update.message.from_user.first_name)

  bot.send_message(chat_id=update.message.chat_id, text="Hi " + update.message.from_user.first_name)

@bot.on_message
def echo(bot, update):
  print(update.message.from_user) # user information such as name and id
  user = db.getUser(update.message.from_user.id)
  print(user)
  bot.send_message(chat_id=update.message.chat_id, text="Hi " + user.username)

bot.start_polling()