from recommendations import get_recommendation_type, recommendation_list, recommendations
from taskallocation import notify_workers
import mongodb as db


def start_question(ctx):
    if len(ctx.user.preferences['course']) > 0:
        ctx.reply(
            "What would you like to receive recommendations on? I can give recommendations on: \n%s" % recommendation_list())
        ctx.user.set_state('asking')
    else:
        ctx.reply("Please add courses to your preference list to get recommendation")
        ctx.user.set_state('modeling')


def handle_question(ctx):
    recommendation_type = get_recommendation_type(ctx.message)
    ctx.user.set_state('idle')

    if(db.get_task(recommendation_type, ctx.user.id, False)):
       ctx.reply("I will get back to you when I have recommendations of `%s` for you %s." % (recommendations[recommendation_type]['name'], ctx.user.name))
       return
    task = db.create_task(recommendation_type, ctx.user.id)

    notify_workers(ctx, task, ctx.user.id)
    ctx.reply("I will get back to you when I have recommendations of `%s` for you %s." % (recommendations[recommendation_type]['name'], ctx.user.name))
