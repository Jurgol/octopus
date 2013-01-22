import sys
import vk
import FB
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Form(QDialog):

    def __init__(self, parent = None):
        super(Form, self).__init__(parent)
        
        vkLabel = QLabel("VK credentials")
        vkButton = QPushButton("Connect to Vk account")
        
        fbLabel = QLabel("FB credentials")
        fbButton = QPushButton("Connect to FB account")
        
        twLabel = QLabel("Twitter credentials")
        twButton = QPushButton("Connect to Twitter account")
        
        self.message = QTextEdit("Type your post here")
        
        postButton = QPushButton("&Post")
        quitButton = QPushButton("Quit")
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(postButton)
        buttonLayout.addWidget(quitButton)
        
        layout = QGridLayout()
        layout.addWidget(vkLabel, 0, 0)
        layout.addWidget(vkButton, 1, 0)
        
        layout.addWidget(fbLabel, 2, 0)
        layout.addWidget(fbButton, 3, 0)
        
        layout.addWidget(twLabel, 4, 0)
        layout.addWidget(twButton, 5, 0)

        layout.addWidget(self.message, 6, 0)
        
        layout.addLayout(buttonLayout, 7, 0, 1, 3)
        self.setLayout(layout)
        self.message.setFocus()
        
        self.connect(vkButton, SIGNAL("clicked()"), self.updateVkCredentials)
        self.connect(fbButton, SIGNAL("clicked()"), self.updateFbCredentials)
        self.connect(twButton, SIGNAL("clicked()"), self.updateTwCredentials)
        self.connect(postButton, SIGNAL("clicked()"), self.postMessage)
        self.connect(quitButton, SIGNAL("clicked()"), self.close)
        
        self.setWindowTitle("Octopus")
        
    def updateVkCredentials(self):
        dialog = vk.VkDlg()
        if dialog.exec_():
            self.vk_access_token = dialog.getAccessToken()
    
    def updateFbCredentials(self):
        dialog = FB.FbDlg()
        if dialog.exec_():
            self.fb_access_token = dialog.getAccessToken()
    
    def updateTwCredentials(self):
        pass
    
    def postMessage(self):
        message = unicode(self.message.toPlainText())
        api = vk.VkApi()
        api.vkMessage(message, self.vk_access_token)
        api = FB.FbApi()
        api.fbMessage(message, self.fb_access_token)
        tw_api = twitter.TwitterApi()
        tw_api.twitterMessage(message, self.twitter_client)
        
app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_() 
