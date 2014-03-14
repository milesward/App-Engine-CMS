import webapp2
import cgi
import urllib
import json
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import mail

class Site(ndb.Model):
  site = ndb.StringProperty()

class Database(webapp2.RequestHandler):
    def get(self):
        ndb.Key(Site, 'data').get()
    def post(self):
        old_data = ndb.Key(Site, 'data').get()
        new_data = json.loads(self.request.body).get('content')
        old_data.site = new_data
        Site(content = content).put()

class Login(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('You are logged in: ' + user.nickname())
        else:
            self.redirect(users.create_login_url(self.request.uri))


class Contact(webapp2.RequestHandler):
    def post(self):
        json_data = json.loads(self.request.body)
        data = [json_data.get(x) for x in ['name', 'email', 'message']]
        mail.send_mail(sender='nimajnebs@gmail.com', 
            to='nimajnebs@gmail.com', 
            subject='Contact Form Message', 
            body='From: {} \nEmail: {} \nMessage: {}'.format(*data))
        self.response.out.write('Thanks!  Your message has been sent.')

app = webapp2.WSGIApplication([
  ('/login', Login),
  ('/contact', Contact),
  ('/database', Database)
])