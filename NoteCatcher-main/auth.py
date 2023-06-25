import pyrebase
import requests
import json

# Please Follow Detailed Explanation from Readme
# Paste your Friebase Details here
# !!! VERY IMPORTANT !!!
CONFIG = {
    apiKey: "AIzaSyBKGggrDOX7PDvizuN79OC9enDoBbnhlhQ",
    authDomain: "todolistapp-5dcbf.firebaseapp.com",
    databaseURL: "https://todolistapp-5dcbf-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "todolistapp-5dcbf",
    storageBucket: "todolistapp-5dcbf.appspot.com",
    messagingSenderId: "788420521087",
    appId: "1:788420521087:web:7609ea0315621ac2bba34a",
    measurementId: "G-1PG6NP03LZ"
  }

firebase = pyrebase.initialize_app(CONFIG)
auth = firebase.auth()
db = firebase.database()
db = firebase.database()

def new_user(email, password):
  try:
    user = auth.create_user_with_email_and_password(email, password)
  except requests.HTTPError as e:
    error_json = e.args[1]
    error = json.loads(error_json)['error']['message']
    if error == "EMAIL_EXISTS":
      return -1, 'Email Already Exists, Try Again'
    else:
      return -1, 'Something Went Wrong'
  else:
    db.child(user['localId']).set('')
    return 0, user['localId']

def Login(email, password):
  try:
    user = auth.sign_in_with_email_and_password(email, password)
  except requests.HTTPError as e:
    error_json = e.args[1]
    error = json.loads(error_json)['error']['message']
    if error == "EMAIL_NOT_FOUND":
      return -1, 'Email is not registered, Try again'
    else:
      return -1,'Wrong Password Try again'
  else:
    return 0, user['localId']

def get_notes(id):
  user = db.child(id).get()

  if user.each() is None:
    return 0, dict()

  notes = dict()
  for note in user.each():
    if note.val() != None:
        notes[note.key()] = note.val()

  return len(notes), notes

def remove_note(id, note):
  db.child(id).child(note).remove()

def add_note(id, note):
  noteid = db.child(id).push(note)
  return noteid['name']
