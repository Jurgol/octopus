from rauth.service import OAuth2Service
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import re
import webbrowser
import vkontakte

class VkDlg(QDialog):
    def __init__(self, parent=None):
        super(VkDlg, self).__init__(parent)
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
        
        self.setWindowTitle("VK credentials")
                
    def getUrl(self):
        vkontakte = OAuth2Service(
            name='vkontakte',
            authorize_url='http://oauth.vk.com/authorize',
            access_token_url='https://api.vk.com/oauth/access_token',
            base_url='https://graph.facebook.com/',
            consumer_key='3358214',
            consumer_secret='Wbn1pOKXLsWloAfNXL4Z')
    
        redirect_uri = 'http://oauth.vk.com/blank.html'
        authorize_url = vkontakte.get_authorize_url(redirect_uri=redirect_uri,
            scope='8192',
            response_type='token')
    
        webbrowser.open(authorize_url)
        return 'Visit URL opened in your browser'
        
    def accept(self):
        url_with_code = unicode(self.tokenedit.text())
        self.access_token = re.search('\#access_token=([^&]*)', url_with_code).group(1)
        QDialog.accept(self)
    
    def getAccessToken(self):
        return self.access_token

class VkApi():
    def vkMessage(self, message_text, VK_access_token):
        vk = vkontakte.API(token = VK_access_token)
        vk.wall.post(message = message_text)
