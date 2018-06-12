import datetime

try:
  from pymongo import MongoClient
except ImportError:
    print('MyCI requires pymongo library.\n')
    sys.exit()


client = MongoClient()
db = client.chatbot

def get_user(user_id, user_name=None, chat_id=None):
  user = db.user.find_one({'userid': user_id})
  if(not user):
    create_user(user_id, user_name, chat_id)
    user = db.user.find_one({'userid': user_id})
  return User(user)

def create_user(user_id, username, chat_id):
  model = {
    'userid': user_id,
    'chatid': chat_id,
    'username': username,
    'state': 'idle',
    'incentive': 0,
    'preferences': {
      'course': []
    },
    'task': None
  }
  db.user.insert_one(model)

def update_user(user_id, model):
  db.user.update_one({'userid': user_id}, {'$set': model})

def update_incentive(user_id, value):
  db.user.update_one({'userid': user_id}, {'incentive': value})

def get_all_users():
  return db.user.find({'state': 'idle'})

def create_task(task_type, user_id):
  task_id = db.task.insert_one({
    'type': task_type,
    'user': user_id,
    'date': datetime.datetime.utcnow(),
    'finished': False,
    'answers': []
  })

  return Task(db.task.find_one({'_id': task_id.inserted_id}))

def get_task(task_type, user_id, finished):
  task = db.task.find_one({'type': task_type, 'user': user_id, 'finished': finished})
  if(task):
    return Task(task)


def update_task(task_id, model):
  db.task.update_one({'_id': task_id}, {'$set': model})

class User:
  def __init__(self, user):
    self.id = user['userid']
    self.name = user['username']
    self.state = user['state']
    self.incentive = user['incentive']
    self.preferences = user['preferences']
    self.chat_id = user['chatid']
    self.task = user['task']


  # User's conversation state (idle, asking, answering, modeling)
  def set_state(self, state):
    self.state = state
    update_user(self.id, {'state': state})

  def get_task(self):
    task = db.task.find_one({'_id': self.task})
    if(task):
      return Task(task)

  def give_task(self, task):
    self.task = task.id
    self.set_state('answering')
    update_user(self.id, {'task': task.id})

  def conclude_task(self):
    self.task = None
    self.set_state('idle')
    update_user(self.id ,{'task': None})

  def save_preference(self, pref_type, preference):
    preferences = set(self.preferences[pref_type])
    preferences.add(preference)
    self.preferences[pref_type] = list(preferences)
    update_user(self.id, {'preferences': self.preferences})

  def send_message(self, ctx, message):
    ctx.send_message(self.chat_id, message)

  def del_preference(self, pref_type, preference):
    preferences = set(self.preferences[pref_type])
    preferences.remove(preference)
    self.preferences[pref_type] = list(preferences)
    update_user(self.id, {'preferences': self.preferences})

class Task:
  def __init__(self, task):
    self.id = task['_id']
    self.type = task['type']
    self.user = get_user(task['user'])
    self.finished = task['finished']
    self.preferences = self.user.preferences[task['type']]
    self.date = task['date']
    self.answers = task['answers']

  def get_pref(self):
    return self.user

  def save_answer(self, answer, user):
    worker = user
    user_pref = set(self.preferences)
    worker_pref = set(worker.preferences[self.type])
    similarity = len(user_pref.intersection(worker_pref))
    self.answers.append([answer,similarity])
    worker.conclude_task()
    update_task(self.id, {'answers': self.answers})

  def finish(self):
    self.finished = True
    update_task(self.id, {'finished': True})
