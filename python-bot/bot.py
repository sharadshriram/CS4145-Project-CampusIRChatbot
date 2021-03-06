try:
  from telegram.ext import Updater
  from telegram.ext import CommandHandler
  from telegram.ext import MessageHandler, Filters
except ImportError:
    print("MyCI requires python-telegram-bot library.\n")
    sys.exit()

import mongodb as db

class Bot:

  def __init__(self, token=None):
    self.updater = Updater(token=token)
    self.dispatcher = self.updater.dispatcher

  def start_polling(self):
    self.updater.start_polling()

  def command(self, command_name):
    def decorator(command_function):
      def handler_function(bot, update):
        ctx = Context(bot, update)
        if(ctx.user.state == 'idle'):
          command_function(Context(bot, update))
        else:
          ctx.reply('Please finish answering the question first.')
      handler = CommandHandler(command_name, handler_function)
      self.dispatcher.add_handler(handler)
    return decorator

  def on_message(self, message_function):
    def handler_function(bot, update):
        message_function(Context(bot, update))
    handler = MessageHandler(Filters.text, handler_function)
    self.dispatcher.add_handler(handler)

class Context:
  def __init__(self, bot, update):
    self.chat_id = update.message.chat_id
    self.message = update.message.text
    self.user = update.message.from_user
    self.user = db.get_user(update.message.from_user.id,
    user_name=update.message.from_user.first_name,
    chat_id=update.message.chat_id)
    self._bot = bot

  def reply(self, message):
    self._bot.send_message(self.chat_id, text=message, parse_mode='Markdown')

  def send_message(self, chat_id, message):
    self._bot.send_message(chat_id, text=message, parse_mode='Markdown')