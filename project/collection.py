
import mysql
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox


def login(self):
    EMAIL = self.email.text()
    PASSWORD = self.password.text()

    # to connect with database .
    con =mysql.connector.connect(user='root',password='ammar45',host='localhost',database='user')
    # Create a Cursor object to execute queries.
    manager = con.cursor()
    get_email = ("SELECT email FROM users WHERE email = '%s'"%str(EMAIL))
    get_password = ("SELECT pass FROM users WHERE password = '%s'"%str(PASSWORD))
    manager.execute(get_email,get_password)

    if self.email.text()== get_email and self.password.text() == get_password:
        msg = QMessageBox()
        msg.setText("successfull login ")
        msg.exec_()
    else:
        msg = QMessageBox()
        msg.setText("check your username or password")
        msg.exec_()

#-------------------------------------------------------------------------
def signup(self):
    try:
        con =mysql.connector.connect(user='root',password='ammar45',host='localhost',database='user')
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
    



