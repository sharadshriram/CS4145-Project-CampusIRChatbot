import mongodb as db
from recommendations import get_course_names
def notify_workers(ctx, task, requester_id):
  users = db.get_all_users()
  users = [user for user in users if user['userid'] != requester_id]
  user_pref = set(task.preferences)
  for user in users:
    #print(user)
    user = db.User(user)
    crowd_pref = set(user.preferences[task.type])

    if(user_pref.intersection(crowd_pref)):
      user.give_task(task)
      user.send_message(ctx, 'Hi, Can you give me some recommendation based on the courses: \n %s' % get_course_names(user_pref.intersection(crowd_pref)))

