#LOreal Likourgos
#IS640 Project

__author__ = "LOreal Likourgos"


import wsgiref.handlers
from google.appengine.api import urlfetch
import webapp2

urlfetch.set_default_fetch_deadline(60)


########## CHANGE THESE TO REFLECT YOUR PERSONAL SETTINGS ##############
# Your Dropbox user-id  and folder-name. 
# Your public folder will have the following syntax: 
# dl.dropboxusercontent.com/u/<USERID>/<YOURFOLDER>/examplefile
# If you want to use the entire "Public" folder, set DROPBOX_FOLDER = ""
DROPBOX_USERID = "1988gtachick@gmail.com"
DROPBOX_FOLDER = "https://www.dropbox.com/sh/g3xzguwn9rdyu6c/AABK9p4yER5VnRENRkY1HsXTa?dl=0"
########################################################################


class DboxHandler(webapp2.RequestHandler):
  def get(self, url_path):
    slash_position = self.request.url.find("/", len(self.request.scheme + "://"))
    if slash_position == -1:
      dropbox_url = "https://"
    else:
      dropbox_path = "" if DROPBOX_FOLDER == "" else "/" + DROPBOX_FOLDER
      dropbox_url = "https://dl.dropbox.com/u/" + DROPBOX_USERID + dropbox_path + self.request.url[slash_position:]

    fetched = urlfetch.fetch(dropbox_url)

    if fetched.status_code == 200:
      for key, value in fetched.headers.iteritems():
        self.response.headers[key] = value
      self.response.out.write(fetched.content)

    else:
      self.response.status = fetched.status_code
      self.response.out.write("Error: status code:" + str(fetched.status_code))


class IndexPageHandler(webapp2.RequestHandler):
  def get(self, base_url=None):
    #Use HTML code below to conjure link to dropbox
	self.response.out.write("<html><body>")
	self.response.out.write("<p>Welcome to Nimbus Store</p>")
	self.response.out.write("<p>Click <a href= DROPBOX_FOLDER> HERE </a> to access my files.</p>")
	self.response.out.write("</body></html>")
	
app = webapp2.WSGIApplication([
  (r"/", IndexPageHandler),
  (r"/(.*)", DboxHandler)
], debug=False)

# Base code cited to Arjun Sreedharan