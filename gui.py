import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Form(QDialog):

    def __init__(self, parent = None):
        super(Form, self).__init__(parent)
        
        vklabel = QLabel("VK credentials")
        self.vkbutton = QPushButton("Connect to Vk account")
        
        fblabel = QLabel("FB credentials")
        self.fbbutton = QPushButton("Connect to FB account")
        
        twlabel = QLabel("Twitter credentials")
        self.twbutton = QPushButton("Connect to Twitter account")
        
        self.message = QTextEdit("Type your post here")
        
        okButton = QPushButton("&Post")
        cancelButton = QPushButton("Exit")
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)
        
        layout = QGridLayout()
        layout.addWidget(vklabel, 0, 0)
        layout.addWidget(self.vkbutton, 1, 0)
        
        layout.addWidget(fblabel, 2, 0)
        layout.addWidget(self.fbbutton, 3, 0)
        
        layout.addWidget(twlabel, 4, 0)
        layout.addWidget(self.twbutton, 5, 0)

        layout.addWidget(self.message, 6, 0)
        
        layout.addLayout(buttonLayout, 7, 0, 1, 3)
        self.setLayout(layout)
        self.message.setFocus()
        
        self.setWindowTitle("Octopus")
        
app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_() 
