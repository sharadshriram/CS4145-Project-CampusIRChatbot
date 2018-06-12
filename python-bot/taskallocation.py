import mongodb as db
from recommendations import get_course_names
import requests
import json

apiKey = "qY1XwzwEysfsaynAQQTq"
job_title= "MyCI - Course Recommendation Task"
instructions="<h1>Overview</h1><p>Please suggst as a course for the question.</p><hr><h1>Steps</h1><p>1. Read the question, describing the task.</p><p>2. Write down a course you'd recommend.</p><p>5. Do this for all questions.</p><p>6. Submit your work.</p><hr>"
request_url = "https://api.figure-eight.com/v1/jobs.json"
headers = {'content-type': 'application/json'}

#create a figure 8 task:
def createWebTask(task):
    cml="""<div class="html-element-wrapper"><p>"""+task+"""<br /></p></div>
    <cml:text label="Your recommended course" validates="required" name="recommended_courses" aggregation="all" gold="true" />"""
    payload = {
    'key': apiKey,
    'job':{
      'title': job_title,
      'instructions': instructions,
      'cml': cml
      }
    }
    response=requests.post(request_url, data=json.dumps(payload), headers=headers)
    print(response)

requesterId = None

#create a task through the chat interface:
def notify_workers(ctx, task, requester_id):
  users = db.get_all_users()
  #filter out the requester
  users = [user for user in users if user['userid'] != requester_id]
  user_pref = set(task.preferences)
  requesterId = requester_id

  for user in users:
    print(user)
    user = db.User(user)
    crowd_pref = set(user.preferences[task.type])

    #simple intersection based model - matching the right worker based on courses
    if(user_pref.intersection(crowd_pref)):
      user.give_task(task)
      user.send_message(ctx, 'Hi, I am looking for a course recommendation for a student that liked: \n %s' % get_course_names(user_pref))
      createWebTask('I am looking for a course recommendation for a student that liked: \n %s' % get_course_names(user_pref))


    



