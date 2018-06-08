
import logging
import settings
from bot import Bot
from usermodel import start_model, handle_model
from question import start_question, handle_question
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=settings.LOGLEVEL)

bot = Bot(token=settings.TOKEN)

@bot.on_message
def on_message(ctx):

  if(ctx.user.state == "asking"):
    handle_question(ctx) # Figure out what user wants here
    return
  if(ctx.user.state == "answering"):
    handle_answer(ctx) # Figure out crowdsourcer's answer here
    return
  if(ctx.user.state == "modeling"):
    handle_model(ctx) # Handle preferences here
    return
  if(ctx.user.state == "idle"):
    handle_idle(ctx) # Figure out new state here

def handle_idle(ctx):
  echo(ctx)

def handle_answer(ctx):
  echo(ctx)

# placeholder
def echo(ctx):
  ctx.reply("Hi " + ctx.user.name)

# start user modeling state
@bot.command('start')
def start(ctx):
  start_model(ctx)

# start recommendation here
@bot.command('recommend')
def recommend(ctx):
  start_question(ctx)

bot.start_polling()