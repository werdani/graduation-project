from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtCore import *  
from PyQt5 import QtWidgets
import threading

import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
import resource
# from model import Model
from out_window import Ui_OutputDialog
from register import Ui_register
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QApplication, QWidget

class Ui_loginfor(QDialog):
    def __init__(self,parent=None):
        super(Ui_loginfor, self).__init__(parent)
        loadUi("login.ui", self)
        self.setMouseTracking(True)
        self.setWindowTitle("XDTeam ")
        self.login.clicked.connect(self.runSlot)
        self.registerbut.clicked.connect(self.regester)

        self.login.setToolTip('This is a tooltip message.')  
        shadow = QGraphicsDropShadowEffect()
        # setting blur radius
        shadow.setOffset(2, 2)
        shadow.setColor(QColor(255, 255, 255))
        shadow.setBlurRadius(17)
        #self.login.setGraphicsEffect(shadow)
        self._new_window = None
        self.Videocapture_ = None

    def refreshAll(self):
        """
        Set the text of lineEdit once it's valid
        """
        self.Videocapture_ = "1"

    @pyqtSlot()
    def runSlot(self):
        self.refreshAll()
        ui.hide()  # hide the main window
        self.outputWindow_()  # Create and open new output window
        
    
    def regester(self):
        self._new_window = Ui_register()
        self._new_window.show()
        
        
    def outputWindow_(self):
        """
        Created new window for vidual output of the video in GUI
        """
        self._new_window = Ui_OutputDialog()
        self._new_window.show()
        self._new_window.startVideo(self.Videocapture_)

        print("Video Played")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_loginfor()
    ui.show()
    sys.exit(app.exec_())


    