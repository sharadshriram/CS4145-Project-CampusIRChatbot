import mongodb as db
from recommendations import get_course_names
def notify_workers(ctx, task):
  users = db.get_all_users()
  user_pref = set(task.preferences)

  for user in users:
    print(user)
    user = db.User(user)
    crowd_pref = set(user.preferences[task.type])

    if(user.id == ctx.user.id):
      continue

    if(user_pref.intersection(crowd_pref)):
      user.give_task(task)
      user.send_message(ctx, 'Hi, I am looking for a course recommendation for a student that liked: \n %s' % get_course_names(user_pref))
