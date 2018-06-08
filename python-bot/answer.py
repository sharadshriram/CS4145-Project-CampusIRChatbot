from difflib import get_close_matches
from recommendations import recommendations, recommendation_list

courses = recommendations['course']['options']

# pending course confirmations for users
pending = {}

def handle_answer(ctx):
  user_id = ctx.user.id
  if user_id in pending.keys():
    closest = get_close_matches(ctx.message, ['yes','no'], cutoff=0)[0]
    if closest == 'yes':
      reply = 'Added `%s` to my survey. Thank you for your answer!' % (pending[user_id] + ' ' + courses[pending[user_id]])
      ctx.user.get_task().save_answer(pending[user_id], user_id)
    else:
      reply = 'What course would you recommend?'
    del pending[user_id]
    ctx.reply(reply)

  else:
    closest = get_close_matches(ctx.message, [code + ' ' + courses[code] for code in courses], cutoff=0)[0]
    reply = "Did you mean the course: `%s`" % closest
    coursecode = closest.split(' ')[0]
    ctx.reply(reply)
    pending[user_id] = coursecode