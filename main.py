import webapp2
import os
import json
import cgi
import urllib
from google.appengine.ext import ndb
from google.appengine.api import users


class Greeting(ndb.Model):
  """Models an individual Guestbook entry with content and date."""
  content = ndb.StringProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)

  @classmethod
  def query_book(cls, ancestor_key):
    return cls.query(ancestor=ancestor_key).order(-cls.date)

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write('<html><body>')
    guestbook_name = self.request.get('guestbook_name')
    ancestor_key = ndb.Key("Book", guestbook_name or "*notitle*")
    greetings = Greeting.query_book(ancestor_key).fetch(20)

    for greeting in greetings:
      self.response.out.write('<blockquote>%s</blockquote>' %
                              cgi.escape(greeting.content))

    self.response.out.write("""
          <form action="/sign?%s" method="post">
            <div><textarea name="content" rows="3" cols="60"></textarea></div>
            <div><input type="submit" value="Sign Guestbook"></div>
          </form>
          <hr>
          <form>Guestbook name: <input value="%s" name="guestbook_name">
          <input type="submit" value="switch"></form>
        </body>
      </html>""" % (urllib.urlencode({'guestbook_name': guestbook_name}),
                    cgi.escape(guestbook_name)))

class SubmitForm(webapp2.RequestHandler):
  def post(self):
    # We set the parent key on each 'Greeting' to ensure each guestbook's
    # greetings are in the same entity group.
    guestbook_name = self.request.get('guestbook_name')
    greeting = Greeting(parent=ndb.Key("Book", guestbook_name or "*notitle*"),
                        content = self.request.get('content'))
    greeting.put()
    self.redirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))

class JSON_Handler(webapp2.RequestHandler):
    def get(self, page):
        # Return the data for a url formatted as JSON

        # page_key = ndb.Key('site', url)
        # page_data = asdfasdf.query_databse(page_key)
        # json.dumps([page.to_dict() for page in Page.query(Page.name == url).fetch()])
        self.response.out.write('JSON Get')

    def post(self, page):
        # Post a the data for a url to the database

        # page = Page(parent=ndb.Key('site', url), content = self.request.get('content'))
        # page.put()
        self.response.write('JSON Post')

class User_Handler(webapp2.RequestHandler):
    def get(self, url):
        self.response.out.write('User Get')
    def post(self, url):
        self.response.out.write('User Post')


# app = webapp2.WSGIApplication([('/json/(.*)', JSON_Handler), ('/user/(.*)', User_Handler)], debug=True)
# app = webapp2.WSGIApplication([('/', MainPage), ('/sign', SubmitForm)])
app = webapp2.WSGIApplication([('/mail/(.*)', Mail_Handler)], debug=True)
