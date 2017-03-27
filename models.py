from google.appengine.ext import ndb

class Visit(ndb.Model):
    user_ip = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    action = ndb.StringProperty()

class Task(ndb.Model):
    controller = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    target = ndb.StringProperty()
    action = ndb.StringProperty()
    done = ndb.BooleanProperty(default=False)
    modded = ndb.DateTimeProperty(auto_now=True)
    notes = ndb.StringProperty()

class User(ndb.Model):
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    lastlogin = ndb.DateTimeProperty()

class Device(ndb.Model):
    name = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    lastseen = ndb.DateTimeProperty()

class Server(ndb.Model):
    name = ndb.StringProperty()
    pin = ndb.StringProperty()
    controller = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    lastseen = ndb.DateTimeProperty()