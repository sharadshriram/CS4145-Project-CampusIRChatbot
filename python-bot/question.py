import operator
from threading import Timer
from recommendations import get_recommendation_type, recommendation_list, recommendations, get_course_names
from taskallocation import notify_workers
import mongodb as db
from settings import DELAY

def start_question(ctx):
  ctx.reply("What would you like to receive recommendations on? I can give recommendations on: \n%s" % recommendation_list())
  ctx.user.set_state('asking')

def handle_question(ctx):
  recommendation_type = get_recommendation_type(ctx.message)
  ctx.user.set_state('idle')

  if(db.get_task(recommendation_type, ctx.user.id)):
    ctx.reply("I am already looking for a recommendation for you on `%s`, I will come back to you with an answer later." % recommendations[recommendation_type]['name'])
    return
  task = db.create_task(recommendation_type, ctx.user.id)

  notify_workers(ctx, task)
  ctx.reply("We will start asking around for recommendations on `%s`!" % recommendations[recommendation_type]['name'])

  def callback():
    task = db.get_task(recommendation_type, ctx.user.id)
    ctx.reply(aggregate_answer(task))
    task.finish()

  t = Timer(DELAY, callback)
  t.start()

def aggregate_answer(task):
  results = {}

  for answer in task.answers:
    if not answer[0] in results.keys():
      results[answer[0]] = 0
    results[answer[0]] += answer[1]
    
  sorted_results = sorted(results.items(), key=operator.itemgetter(1))

  return 'My top result is: %s' % get_course_names([sorted_results[0][0]])