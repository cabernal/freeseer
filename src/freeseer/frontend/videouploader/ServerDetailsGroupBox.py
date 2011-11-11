'''
Created on Oct 15, 2011

@author: jord
'''

from PyQt4 import QtCore, QtGui

class ServerDetailsGroupBox(QtGui.QGroupBox):
    '''
    classdocs
    '''
    
    Sftp, Drupal = range(2)
    
    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QtGui.QGroupBox.__init__(self, parent)
        
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.formLayout_serverdetails = QtGui.QFormLayout()
        self.formLayout_serverdetails.setObjectName("formLayout_serverdetails")
        
        self.label_username = QtGui.QLabel(self)
        self.label_username.setObjectName("label_username")
        self.formLayout_serverdetails.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_username)
        
        self.label_password = QtGui.QLabel(self)
        self.label_password.setObjectName("label_password")
        self.formLayout_serverdetails.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_password)
        
        self.label_Server = QtGui.QLabel(self)
        self.label_Server.setObjectName("label_Server")
        self.formLayout_serverdetails.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_Server)
        
        self.horizontalLayout_serveraddress = QtGui.QHBoxLayout()
        self.horizontalLayout_serveraddress.setObjectName("horizontalLayout_serveraddress")
        
        self.lineEdit_Server = QtGui.QLineEdit(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_Server.sizePolicy().hasHeightForWidth())
        self.lineEdit_Server.setSizePolicy(sizePolicy)
        self.lineEdit_Server.setMinimumSize(QtCore.QSize(150, 0))
        self.lineEdit_Server.setObjectName("lineEdit_Server")
        self.horizontalLayout_serveraddress.addWidget(self.lineEdit_Server)
        
        self.label_port = QtGui.QLabel(self)
        self.label_port.setObjectName("label_port")
        self.horizontalLayout_serveraddress.addWidget(self.label_port)
        
        self.lineEdit_port = QtGui.QLineEdit(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_port.sizePolicy().hasHeightForWidth())
        self.lineEdit_port.setSizePolicy(sizePolicy)
        self.lineEdit_port.setMinimumSize(QtCore.QSize(50, 0))
        self.lineEdit_port.setObjectName("lineEdit_port")
        self.horizontalLayout_serveraddress.addWidget(self.lineEdit_port)
        
        self.formLayout_serverdetails.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout_serveraddress)
        self.lineEdit_password = QtGui.QLineEdit(self)
        self.lineEdit_password.setText("")
        self.lineEdit_password.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.formLayout_serverdetails.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_password)
        
        self.lineEdit_username = QtGui.QLineEdit(self)
        self.lineEdit_username.setObjectName("lineEdit_username")
        self.formLayout_serverdetails.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_username)
        
        self.verticalLayout.addLayout(self.formLayout_serverdetails)
        
        self.horizontalLayout_servertype = QtGui.QHBoxLayout()
        self.horizontalLayout_servertype.setObjectName("horizontalLayout_servertype")
        
        self.radioButton_sftp = QtGui.QRadioButton(self)
        self.radioButton_sftp.setObjectName("radioButton_sftp")
        self.horizontalLayout_servertype.addWidget(self.radioButton_sftp)
        
        self.radioButton_drupal = QtGui.QRadioButton(self)
        self.radioButton_drupal.setObjectName("radioButton_drupal")
        self.horizontalLayout_servertype.addWidget(self.radioButton_drupal)
        
        self.buttonGroup_serverType = QtGui.QButtonGroup(self)
        self.buttonGroup_serverType.addButton(self.radioButton_sftp)
        self.buttonGroup_serverType.addButton(self.radioButton_drupal)
        
        self.verticalLayout.addLayout(self.horizontalLayout_servertype)
        
        self.retranslate()
        
        # radiobutton mapping #
        self.serverType_button_mapping = {self.Sftp:   self.radioButton_sftp,
                                          self.Drupal: self.radioButton_drupal}
        
        self.button_serverType_mapping = dict(reversed(item) for item in self.serverType_button_mapping.items())
    
    def retranslate(self):
        self.setTitle(self.tr("Server Details"))
        self.label_username.setText(self.tr("Username"))
        self.label_password.setText(self.tr("Password"))
        self.label_Server.setText(self.tr("Server"))
        self.label_port.setText(self.tr("Port"))
        self.radioButton_sftp.setText(self.tr("SFTP/SCP"))
        self.radioButton_drupal.setText(self.tr("Drupal"))
        
    def getUsername(self):
        return self.lineEdit_username.text()
    def setUsername(self, value):
        self.lineEdit_username.setText(value)
    username = property(getUsername, setUsername)
    
    def getPassword(self):
        return self.lineEdit_password.text()
    password = property(getPassword)
    
    def getServerAddress(self):
        return self.lineEdit_Server.text()
    def setServerAddress(self, value):
        self.lineEdit_Server.setText(value)
    serverAddress = property(getServerAddress, setServerAddress)
    
    def getServerPort(self):
        return self.lineEdit_port.text()
    def setServerPort(self, value):
        self.lineEdit_port.setText(value)
    serverPort = property(getServerPort, setServerPort)
        
    def getServerType(self):
        return self.button_serverType_mapping[self.buttonGroup_serverType.checkedButton()]
    def setServerType(self, value):
        self.serverType_button_mapping[value].click()
    serverType = property(getServerType, setServerType)
    
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = ServerDetailsGroupBox()
    main.show()
    sys.exit(app.exec_())