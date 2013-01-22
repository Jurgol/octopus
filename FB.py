__author__ = 'Jury Golovan'

from rauth.service import OAuth2Service
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import re
import webbrowser
import facebook


class FbDlg(QDialog):
    def __init__(self, parent=None):
        super(FbDlg, self).__init__(parent)
        self.urllabel = QLabel(self.getUrl())
        self.tokenedit = QLineEdit("Copy URL from your browser's address bar")

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)

        layout = QGridLayout()
        layout.addWidget(self.urllabel, 0, 0)
        layout.addWidget(self.tokenedit, 1, 0)
        layout.addWidget(buttonBox, 2, 0, 1, 2)
        self.setLayout(layout)
        self.tokenedit.selectAll()
        self.tokenedit.setFocus()

        self.connect(buttonBox, SIGNAL("accepted()"),
            self, SLOT("accept()"))
        self.connect(buttonBox, SIGNAL("rejected()"),
            self, SLOT("reject()"))

        self.setWindowTitle("FB credentials")

    def getUrl(self):
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

        webbrowser.open(authorize_url)
        return 'Visit URL opened in your browser'

    def accept(self):
        url_with_code = unicode(self.tokenedit.text())
        self.access_token = re.search('\#access_token=([^&]*)', url_with_code).group(1)
        QDialog.accept(self)

    def getAccessToken(self):
        return self.access_token

class FbApi():
    def fbMessage(self, message_text, FB_access_token):
        graph = facebook.GraphAPI(FB_access_token)
        graph.put_object("me", "feed", message = message_text)


