try:
  from telegram.ext import Updater
  from telegram.ext import CommandHandler
  from telegram.ext import MessageHandler, Filters
except ImportError:
    print("MyCI requires python-telegram-bot library.\n")
    sys.exit()

class Bot:

  def __init__(self, token=None):
    self.updater = Updater(token=token)
    self.dispatcher = self.updater.dispatcher

  def start_polling(self):
    self.updater.start_polling()

  def command(self, command_name):
    def decorator(command_function):
      handler = CommandHandler(command_name, command_function)
      self.dispatcher.add_handler(handler)
    return decorator

  def on_message(self, message_function):
    handler = MessageHandler(Filters.text, message_function)
    self.dispatcher.add_handler(handler)