'''
Created on 22.01.2013

@author: pzaytsev
'''
from PyQt4 import QtGui, QtCore
import webbrowser
import oauth2 as oauth
import urlparse
import urllib

class TwitterDlg(QtGui.QDialog):
    def __init__(self, parent=None):
        super(TwitterDlg, self).__init__(parent)
        self.urllabel = QtGui.QLabel(self.getUrl())
        self.tokenedit = QtGui.QLineEdit("Copy PIN")
        
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel)
        
        layout = QtGui.QGridLayout()
        layout.addWidget(self.urllabel, 0, 0)
        layout.addWidget(self.tokenedit, 1, 0)
        layout.addWidget(buttonBox, 2, 0, 1, 2)
        self.setLayout(layout)
        self.tokenedit.selectAll()
        self.tokenedit.setFocus()
        
        self.connect(buttonBox, QtCore.SIGNAL("accepted()"),
                     self, QtCore.SLOT("accept()"))
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"),
                     self, QtCore.SLOT("reject()"))
        
        self.setWindowTitle("Twitter credentials")
        
    def getUrl(self):
        consumer_key = 'QhPt0WI3dpVuRcNXyHLJKQ'
        consumer_secret = 'ZnZEVx1BSERrBF4mSO98e02LyGa5SbOe1AA7v0wU'
        request_token_url = 'https://api.twitter.com/oauth/request_token'
        authorize_url =     'https://api.twitter.com/oauth/authorize'
        self.consumer = oauth.Consumer(consumer_key, consumer_secret)
        client = oauth.Client(self.consumer)
        resp, content = client.request(request_token_url, "POST", headers = {})
        if resp.status >= 200 and resp.status <=300:
            self.request_token = dict(urlparse.parse_qsl(content))
            authorize_url = authorize_url + "?oauth_token=" + self.request_token['oauth_token']
            webbrowser.open(authorize_url)
            return 'Visit URL opened in your browser'
    
    def accept(self):
        access_token_url =  'https://api.twitter.com/oauth/access_token'
        oauth_verifier= unicode(self.tokenedit.text())
        token = oauth.Token(self.request_token['oauth_token'],self.request_token['oauth_token_secret'])
        token.set_verifier(oauth_verifier)
        client = oauth.Client(self.consumer, token)
        resp, content = client.request(access_token_url, "POST", headers = {})
        if resp.status >= 200 and resp.status <=300:
            # parse out the access token
            access_token = dict(urlparse.parse_qsl(content))
            # swap in the new auth token to the client
            token = oauth.Token(key=access_token['oauth_token'],secret=access_token['oauth_token_secret'])
            self.twitter_client = oauth.Client(self.consumer, token)
        else:
            raise Exception(resp.status)
        QtGui.QDialog.accept(self)
        
    def getClient(self):
        return self.twitter_client
    
class TwitterApi():
    def twitterMessage(self, message_text, twitter_client):
        data = {'status': message_text}
        request_uri = 'https://api.twitter.com/1/statuses/update.json'
        resp, content = twitter_client.request('https://api.twitter.com/1/statuses/update.json', 'POST', urllib.urlencode(data))