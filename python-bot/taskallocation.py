import mongodb as db

def notify_workers(ctx, task):
  users = db.get_all_users()

  for user in users:
    print(user)

