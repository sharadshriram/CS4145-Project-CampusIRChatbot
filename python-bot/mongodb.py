try:
  from pymongo import MongoClient
except ImportError:
    print("MyCI requires pymongo library.\n")
    sys.exit()


client = MongoClient()
db = client.chatbot

def get_user(user_id, user_name):
  user = db.user.find_one({"userid": user_id})
  if(not user):
    create_user(user_id, user_name)
    user = db.user.find_one({"userid": user_id})
  return User(user)

def create_user(user_id, username):
  model = {"userid": user_id, "username": username, "state": "idle"}
  db.user.insert_one(model)

def update_user(user_id, model):
  db.user.update_one({"userid": user_id}, {"$set": model})

class User:
  def __init__(self, user):
    self.id = user['userid']
    self.name = user['username']
    self.state = user['state']

  # User's conversation state (idle, asking, answering, modeling)
  def set_state(self, state):
    self.state = state
    update_user(self.id, {"state": state})

