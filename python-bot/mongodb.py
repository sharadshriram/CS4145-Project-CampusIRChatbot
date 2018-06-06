try:
  from pymongo import MongoClient
except ImportError:
    print("MyCI requires pymongo library.\n")
    sys.exit()



class Database:
  def __init__(self):
    self.client = MongoClient()
    self.db = self.client.chatbot
    self.user = self.db.user

  def getUser(self,userid):
    return self.user.find_one({"userid": userid})

  def createUser(self, userid, username):
    model = {"userid": userid, "username": username}
    self.user.insert_one(model)

  def updateUser(self, userid, model):
    self.user.update_one({"userid": userid,model})