'''
Created on 21.01.2013

@author: pzaytsev
'''
import oauth2 as oauth, urllib
import urlparse


def twitter_auth():
    '''
    Authorize user in twitter.
    @author: pzaytsev
    '''
    CONSUMER_KEY = 'QhPt0WI3dpVuRcNXyHLJKQ'
    CONSUMER_SECRET = 'ZnZEVx1BSERrBF4mSO98e02LyGa5SbOe1AA7v0wU'
    #URLs
    REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
    ACCESS_TOKEN_URL =  'https://api.twitter.com/oauth/access_token'
    AUTHORIZE_URL =     'https://api.twitter.com/oauth/authorize'
    # Create out OAuth consumer instance
    consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    client = oauth.Client(consumer)
    resp, content = client.request(REQUEST_TOKEN_URL, "POST", headers = {})
    request_token = dict(urlparse.parse_qsl(content))
    print "Go to the following link in your browser:"
    print "%s?oauth_token=%s" % (AUTHORIZE_URL, request_token['oauth_token'])
    oauth_verifier = raw_input('What is the PIN? ')
    token = oauth.Token(request_token['oauth_token'],request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)
    resp, content = client.request(ACCESS_TOKEN_URL, "POST", headers = {})
    # parse out the access token
    access_token = dict(urlparse.parse_qsl(content))
    # swap in the new auth token to the client
    token = oauth.Token(key=access_token['oauth_token'],secret=access_token['oauth_token_secret'])
    client = oauth.Client(consumer, token)
    return client

def post_message_twitter(client, message):
    resp, content =client.request("https://api.twitter.com/1/statuses/update.json", 
                                  "POST",
                                  body=urllib.urlencode({'status': message}),
                                  headers=None,
                                  force_auth_header=True)
    return content
