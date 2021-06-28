from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtCore import *  
from PyQt5 import QtWidgets
import threading
import mysql
#import _mysql_connector

import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
import resource
from out_window import Ui_OutputDialog

from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QApplication, QWidget

class Ui_register(QDialog):
    def __init__(self,parent=None):
        super(Ui_register, self).__init__(parent)
        loadUi("register.ui", self)
        self.regis.clicked.connect(self.signup)
    
    def signup(self):
        try:
            con =mysql.connector.connect(user='root',password='ammar45',host='localhost',database='user')
            manager   = con.cursor()
            first_name= self.fname.text()
            last_name =  self.lname.text()
            email     =  self.email.text()
            password1 =  self.pass1.text()
            password2 =  self.pass2.text()
            query = "INSERT INTO users (fname,lname,email, pass) VALUES (%s, %s, %s, %s)"
            value = (first_name,last_name,email, password1)
            manager.execute(query, value)
            con.commit()
            print("Data Inserted ")
        except:
            print("errror")
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_register()
    ui.show()
    sys.exit(app.exec_())


    