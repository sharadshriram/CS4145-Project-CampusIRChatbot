
import logging
import settings
from bot import Bot

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=settings.LOGLEVEL)

bot = Bot(token=settings.TOKEN)

@bot.command('start')
def start(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

@bot.on_message
def echo(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

bot.start_polling()