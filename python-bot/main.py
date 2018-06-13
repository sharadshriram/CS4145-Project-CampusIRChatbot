
import logging
import settings
from bot import Bot
from usermodel import start_model, handle_model, start_addpreference, start_removepreference, handle_update, start_displaypreference, start_points
from question import start_question, handle_question
from answer import handle_answer
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=settings.LOGLEVEL)

bot = Bot(token=settings.TOKEN)

@bot.on_message
def on_message(ctx):

  if(ctx.user.state == "asking"):
    handle_question(ctx) # Figure out what user wants here
    return
  if ctx.user.state == "answering":
    handle_answer(ctx) # Figure out crowdsourcer's answer here
    return
  if(ctx.user.state == "modeling"):
    handle_model(ctx) # Handle preferences here
    return
  if(ctx.user.state == "updating"):
    handle_update(ctx) # Handle preferences here
    return
  if(ctx.user.state == "idle"):
    handle_idle(ctx) # Figure out new state here

def handle_idle(ctx):
  ctx.reply("Hi %s, you can use the command /menu!" % ctx.user.name)

# start user modeling state
@bot.command('start')
def start(ctx):
  start_model(ctx)

# start recommendation here
@bot.command('recommend')
def recommend(ctx):
  start_question(ctx)

@bot.command('addpreference')
def addpreference(ctx):
  start_addpreference(ctx)

@bot.command('display')
def displaypreference(ctx):
  start_displaypreference(ctx)

@bot.command('remove')
def removepreference(ctx):
  start_removepreference(ctx)

@bot.command('menu')
def menu(ctx):
  start_menu(ctx)

@bot.command('points')
def points(ctx):
  start_points(ctx)

myci_menu = '''Hello %s
/addpreference to add courses to your preference list
/remove to remove a course from your list
/display to display your current preferences
/recommend to ask request course recommendation
/points to check your current points'''

def start_menu(ctx):
    reply = myci_menu % (ctx.user.name)
    ctx.reply(reply)

bot.start_polling()

