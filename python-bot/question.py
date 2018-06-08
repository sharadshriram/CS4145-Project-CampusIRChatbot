from recommendations import get_recommendation_type, recommendation_list, recommendations
from taskallocation import notify_workers
import mongodb as db

def start_question(ctx):
  ctx.reply("What would you like to receive recommendations on? I can give recommendations on: \n%s" % recommendation_list())
  ctx.user.set_state('asking')

def handle_question(ctx):
  recommendation_type = get_recommendation_type(ctx.message)
  ctx.user.set_state('idle')

  if(db.get_task(recommendation_type, ctx.user.id, False)):
    ctx.reply("I am already looking for a recommendation for you on `%s`, I will come back to you with an answer later." % recommendations[recommendation_type]['name'])
    return
  # db.create_task(recommendation_type, ctx.user.id)

  notify_workers(ctx, None)
  ctx.reply("We will start asking around for recommendations on `%s`!" % recommendations[recommendation_type]['name'])

