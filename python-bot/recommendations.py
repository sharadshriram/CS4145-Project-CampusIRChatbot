import csv
from difflib import get_close_matches

courses = {}
with open('courselist.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile,delimiter=',')
    for row in csvReader:
        courses[row[0]] = row[1]

recommendations = {
  'course' : {
    'name' : 'Courses',
    'question' : "What are some courses that you liked?",
    'options' : courses
  }
}

def recommendation_list():
  res = ""
  for r in recommendations:
    res += '`%s`\n' % recommendations[r]['name']
  return res

def get_recommendation_type(message):
  names = [recommendations[x]['name'] for x in recommendations]
  closest = get_close_matches(message, names, cutoff=0)[0]

  for x in recommendations:
    if recommendations[x]['name'] == closest:
      return x

def get_course_names(user_courses):
  res = ''
  for c in user_courses:
    res += '\n `' + c + ' ' + courses[c] + '`'

  return res