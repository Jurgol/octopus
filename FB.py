__author__ = 'Jury Golovan'
from rauth.service import OAuth2Service
import re
import webbrowser
import facebook

def FB_auth():
    facebook = OAuth2Service(
        name='facebook',
        authorize_url='https://graph.facebook.com/oauth/authorize',
        access_token_url='https://graph.facebook.com/oauth/access_token',
        base_url='https://graph.facebook.com/',
        consumer_key='525099244188735',
        consumer_secret='a01cfffe4b2391fcd78f0702130b494e')

    redirect_uri = 'https://www.facebook.com/connect/login_success.html'
    authorize_url = facebook.get_authorize_url(redirect_uri=redirect_uri,
        scope='read_stream',
        response_type='token')

    print 'Visit this URL in your browser: ' + authorize_url
    webbrowser.open(authorize_url);

    url_with_code = raw_input("Copy URL from your browser's address bar: ")
    FB_access_token = re.search('\#access_token=([^&]*)', url_with_code).group(1)
    return FB_access_token

def FB_message(text):
    graph = facebook.GraphAPI(
        'AAAHdkzHr9D8BAHKmyZBoCbYLg9fk2QjDo9vSDSVFkmNpGIegub18HlAu7QjdNk8TLCXraWZAkYZCsPigls6AwbhomePlXV2CIMhbGI6R3oZAPKwXmZCT3')
    graph.put_object("me", "feed", message = text)


text = 'test'
FB_message(text)
