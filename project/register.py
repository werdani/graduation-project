from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *  
import mysql
import mysql.connector
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog

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
            if (password1 != password2):
                msgBox = QMessageBox()
                msgBox.setText("cheek yor password")
                msgBox.exec_()
            else:
                query = "INSERT INTO users (fname,lname,email, pass) VALUES (%s, %s, %s, %s)"
                value = (first_name,last_name,email, password1)
                manager.execute(query, value)
                con.commit()

                self.fname.setText('')
                self.lname.setText('')
                self.email.setText('')
                self.pass1.setText('')
                self.pass2.setText('')
                msgBox = QMessageBox()
                msgBox.setText("Data Inserted")
                msgBox.exec_()
        except:
            msgBox = QMessageBox()
            msgBox.setText("error")
            msgBox.exec_()
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_register()
    ui.show()
    sys.exit(app.exec_())


    