import os
import json
import requests

from db import DB

default = {
    "first_name": "",
    "last_name": "",
    "gender": "",
    "location": "",
    "profile_pic": "",
    "latitude": "",
    "longitude": "",
    "education": "",
    "occupation": "", 
    "interests": "", 
    "cuisine": "", 
    "preferred_time": ""
}

def init(id):
    with DB() as conn:
        user = conn.findOne("SELECT * FROM users WHERE users.id = %s" % (id))
        if not user:
            user = json.loads(requests.get("https://graph.facebook.com/v2.8/%s?access_token=%s" % (id, os.environ.get("PAGE_ACCESS_TOKEN"))).text)
            insertid = conn.insert("INSERT INTO users (id, first_name, last_name, gender, profile_pic) values (%s, '%s', '%s', '%s', '%s')" % (id, user['first_name'], user['last_name'], user['gender'], user['profile_pic']))
        return True

def updateLoc(id, _lat, _long):
    with DB() as conn:
        return conn.update("UPDATE users SET latitude = %s, longitude = %s, last_message = now() WHERE users.id = %s" % (_lat, _long, id)) > 0

def updateParam(id, name, value):
    allowed = ["latitude", "longitude", "location", "first_name", "last_name", "gender", "profile_pic", "education", "occupation", "interests", "cuisine", "preferred_time"]
    if name not in allowed:
        return False
    if value is None:
        value = ""
    if name == "interests":
        if not value:
            value = []
        value = json.dumps(value)
    with DB() as conn:
        return conn.update("UPDATE users SET %s = '%s', last_message = now() WHERE users.id = %s" % (name, value, id)) > 0

def update(query):
    with DB() as conn:
        return conn.update(query) > 0

def updateUsuals(id, location, cuisine, message):
    if location is None or location == "None":
        location = ""
    if cuisine is None or cuisine == "None":
        cuisine = ""
    if message is None or message == "None":
        message = ""
    return update("UPDATE users SET location = '%s', cuisine = '%s', message = '%s' WHERE id = %s" % (location, cuisine, message, id))

def get(id, as_json=False):
    with DB() as conn:
        user = conn.findOne("SELECT * FROM users WHERE users.id = %s" % (id))
        if not user:
            conn.insert("INSERT into users (id) VALUES (%s)" % (id))
            _temp = default
            _temp["id"] = id
            _temp["userid"] = _temp["id"]
            return _temp
        if "interests" not in user:
            user['interests'] = []
        else:
            if user['interests']:
                user['interests'] = json.loads(user['interests'])
        user['userid'] = user['id']
        if as_json == True:
            return json.dumps(user)
        return user
