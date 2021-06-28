
import mysql
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox


def login(self):
    EMAIL = self.email.text()
    PASSWORD = self.password.text()

    # to connect with database .
    con =mysql.connector.connect(user='ammar45',password='12345',host='localhost',database='user')
    # Create a Cursor object to execute queries.
    manager = con.cursor()
    get_username = ("SELECT username FROM users WHERE email = '%s'"%str(EMAIL))
    get_password = ("SELECT password FROM users WHERE password = '%s'"%str(PASSWORD))
    manager.execute(get_username,get_password)

    if self.username.text()== get_username and self.password.text() == get_password:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("successfull login ")
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("check your username or password")

#-------------------------------------------------------------------------
def signup(self):
    try:
        con =mysql.connector.connect(user='admin',password='12345',host='localhost',database='user')
        manager = con.cursor()
        first_name = self.fname.text()
        last_name =  self.lname.text()
        email     =  self.email.text()
        password1 =  self.password1.text()
        password2 =  self.password2.text()

        if password1 != password2 :
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("check your password")
        query = "INSERT INTO users (first_name,last_name,email, password1,password2) VALUES (%s, %s, %s, %s, %s)"
        value = (first_name,last_name,email, password1,password2)
        manager.execute(query, value)
        con.commit()
        msg.setText("Data Inserted ")
    except:
            msg.setText("Error Inserting Data")
    



