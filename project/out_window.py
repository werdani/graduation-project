from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer, QDate, Qt
from PyQt5.QtWidgets import QDialog,QMessageBox
import cv2
import face_recognition
import numpy as np
import datetime
import os
import csv
import glob
import urllib.request
import urllib.error
import time
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets

import threading
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog
import resource
# from model import Model
#from out_window import Ui_OutputDialog
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QApplication, QWidget

class Ui_OutputDialog(QDialog):
    def __init__(self):
        super(Ui_OutputDialog, self).__init__()
        loadUi("./outputwindow.ui", self)
        #Update time
        self.continueEvent1 = threading.Event()
        self.continueEvent1.clear()

        self.stopEvent = threading.Event()
        self.stopEvent.clear()

        now = QDate.currentDate()
        current_date = now.toString('ddd dd MMMM yyyy')
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.Date_Label.setText(current_date)
        self.Time_Label.setText(current_time)
        self.Bstart.clicked.connect(self.start)
        self.Bstop.clicked.connect(self.stop)
        self.checkInButton.clicked.connect(self.checkIn)
        self.checkOutButton.clicked.connect(self.checkOut)
        self.image = None
 
    @pyqtSlot()
    def startVideo(self, camera_name):
        """
        :param camera_name: link of camera or usb camera
        :return:
        """
        if len(camera_name) == 1:
        	self.capture = cv2.VideoCapture(int(camera_name), cv2.CAP_DSHOW)
        else:
        	self.capture = cv2.VideoCapture(camera_name, cv2.CAP_DSHOW)
        self.timer = QTimer(self)  # Create Timer
        text2 = str(self.comboBox2.currentText())

        print(text2)

        # known face encoding and known face name list
    def stop(self):
        self.NameLabe.setText('stop')
        self.imgLabel.setText(" ")


    def start(self):
            self.NameLabe.setText('start')
            self.capture = cv2.VideoCapture(int(0), cv2.CAP_DSHOW)

            self.checkInButton.setChecked(False)
            self.checkInButton.setEnabled(True)
            path = 'ImagesAttendance'
            if not os.path.exists(path):
                os.mkdir(path)
            images = []
            self.class_names = []
            self.encode_list = []
            self.TimeList1 = []
            self.TimeList2 = []
            attendance_list = os.listdir(path)

            # print(attendance_list)
            for cl in attendance_list:
                cur_img = cv2.imread(f'{path}/{cl}')
                images.append(cur_img)
                x=cl.rsplit('.', 666)
                self.class_names.append(x[0])

            for img in images:
                try:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    boxes = face_recognition.face_locations(img)
                    encodes_cur_frame = face_recognition.face_encodings(img, boxes)[0]
                # encode = face_recognition.face_encodings(img)[0]
                    self.encode_list.append(encodes_cur_frame)
                except Exception as e:
                    print(e)
            if self.NameLabe.text()=='start':

                self.timer.timeout.connect(self.update_frame)  # Connect timeout to the output function
                self.timer.start(500)  # emit the timeout() signal at x=40ms


    def checkIn(self):
            if self.checkInButton.isChecked():
                self.checkInButton.setEnabled(False)
                with open('Attendance.csv', 'a') as f:
                        if (self.NameLabel.text() != '' ):
                            buttonReply = QMessageBox.question(self, 'Welcome ' + self.NameLabel.text(), 'Are you checking In?' ,
                                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                            if buttonReply == QMessageBox.Yes:
                                text = str(self.comboBox.currentText())
                                text2 = str(self.comboBox2.currentText())

                                date_time_string = datetime.datetime.now().strftime("%d/%m/%y, %H:%M:%S")
                                f.writelines(f'\n{self.NameLabel.text()};{date_time_string};{text};{text2};check In')
                                self.checkInButton.setChecked(False)
                                self.StatusLabel.setText('checked In')
                                self.HoursLabel.setText('Measuring')
                                self.MinLabel.setText('')
                                #self.CalculateElapse(idimg)
                                #print('Yes clicked and detected')
                                self.Time1 = datetime.datetime.now()
                                #print(self.Time1)
                                self.checkInButton.setEnabled(True)

                                self.NameLabe2.setText('')
                                self.IDLabel.setText('')
                                self.NameLabel.setText('')
                                self.lvlLabel.setText('')
                                self.StatusLabel.setText('')
                                self.HoursLabel.setText('')
                                self.MinLabel.setText('')

                            else:
                                self.checkInButton.setChecked(False)
                                self.checkInButton.setEnabled(True)

                            time.sleep(1.5)

                        else:
                            buttonReply = QMessageBox.question(self, 'Welcome ' + self.NameLabe.text(), 'You are unknown!' ,
                                                            QMessageBox.Ok  )
                            self.checkInButton.setChecked(False)
                            self.checkInButton.setEnabled(True)


    def checkOut(self):
            if self.checkOutButton.isChecked():
                self.checkOutButton.setEnabled(False)
                with open('Attendance.csv', 'a') as f:
                        if (self.NameLabel.text()!= 'unknown'):
                            buttonReply = QMessageBox.question(self, 'Cheers ' + self.NameLabel.text(), 'Are you checking Out?',
                                                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                            if buttonReply == QMessageBox.Yes:
                                text = str(self.comboBox.currentText())

                                text2 = str(self.comboBox2.currentText())
                                date_time_string = datetime.datetime.now().strftime("%d/%m/%y, %H:%M:%S")
                                f.writelines(f'\n{self.NameLabel.text()};{date_time_string};{text};{text2};check Out')
                                self.checkOutButton.setChecked(False)
                                self.StatusLabel.setText('checked Out')
                                self.Time2 = datetime.datetime.now()
                                #print(self.Time2)

                                self.ElapseList(self.NameLabel.text())
                                self.TimeList2.append(datetime.datetime.now())
                                CheckInTime = self.TimeList1[-1]
                                CheckOutTime = self.TimeList2[-1]
                                self.ElapseHours = (CheckOutTime - CheckInTime)
                                self.MinLabel.setText("{:.0f}".format(abs(self.ElapseHours.total_seconds() / 60)%60) + 'm')
                                self.HoursLabel.setText("{:.0f}".format(abs(self.ElapseHours.total_seconds() / 60**2)) + 'h')
                                self.checkOutButton.setEnabled(True)
                            else:
                                print('Not clicked.')
                                self.checkOutButton.setEnabled(True)

    def face_rec_(self, frame, encode_list_known, class_names):
        """
        :param frame: frame from camera
        :param encode_list_known: known face encoding
        :param class_names: known face names
        :return:
        """
        # csv
        
        def mark_attendance(idimg):
            if self.NameLabel.text()=='':
                text_files = glob.glob( "ImagesAttendance/*.jpg", recursive = True)
                print(text_files)
                print([s.strip('*/') for s in text_files]) # remove the 8 from the string borders
                x=[s.replace('ImagesAttendance\\', '') for s in text_files]
                print(x)
                if idimg!='unknown':
                    h=idimg
                    final_array = [i for i in range(len(x)) if h in x[i]]
                    d=final_array[0]
                    j=x[d] #name.nans.asdsad
                    print(j)
                    k=j.rsplit('.', 666)
                else:
                    self.NameLabe2.setText('0')


            """
            :param name: detected face known or unknown one
            :return:
            """
            if (k[1] != 'unknown'):
                self.NameLabe2.setText('1')
                self.IDLabel.setText(idimg)
                self.NameLabel.setText(k[1])
                self.lvlLabel.setText(k[2])
                with open('Attendance.csv', "r") as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=';')
                    for row in csv_reader:
                        for field in row:
                            self.StatusLabel.setText(field[0:99])
            else:
                self.NameLabe2.setText('0')




        # face recognition
        if self.NameLabe.text()=='start':
            faces_cur_frame = face_recognition.face_locations(frame)
            encodes_cur_frame = face_recognition.face_encodings(frame, faces_cur_frame)
        else:
            print('ooooooooooooooooooooooooooo')
        # count = 0
        for encodeFace, faceLoc in zip(encodes_cur_frame, faces_cur_frame):
            match = face_recognition.compare_faces(encode_list_known, encodeFace, tolerance=0.50)
            face_dis = face_recognition.face_distance(encode_list_known, encodeFace)
            idimg = "unknown"
            best_match_index = np.argmin(face_dis)
            y1, x2, y2, x1 = faceLoc
            # print("s",best_match_index)
            if match[best_match_index]:
                idimg = class_names[best_match_index].upper()
                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 200, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 20), (x2, y2), (0, 200, 0), cv2.FILLED)
                cv2.putText(frame, idimg, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                if  idimg!=self.IDLabel.text():
                        self.NameLabe2.setText('')
                        self.IDLabel.setText('')
                        self.NameLabel.setText('')
                        self.lvlLabel.setText('')
                        self.StatusLabel.setText('')
                        self.HoursLabel.setText('')
                        self.MinLabel.setText('')
            mark_attendance(idimg)

        return frame

    def showdialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("This is a message box")
        msg.setInformativeText("This is additional information")
        msg.setWindowTitle("MessageBox demo")
        msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)



    def ElapseList(self,name):
        with open('Attendance.csv', "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 2

            Time1 = datetime.datetime.now()
            Time2 = datetime.datetime.now()
            for row in csv_reader:
                for field in row:
                    if field in row:
                        if field == 'check In':
                            if row[0] == name:
                                #print(f'\t ROW 0 {row[0]}  ROW 1 {row[1]} ROW2 {row[2]}.')
                                Time1 = (datetime.datetime.strptime(row[1], '%d/%m/%y, %H:%M:%S'))
                                self.TimeList1.append(Time1)
                        if field == 'check Out':
                            if row[0] == name:
                                #print(f'\t ROW 0 {row[0]}  ROW 1 {row[1]} ROW2 {row[2]}.')
                                Time2 = (datetime.datetime.strptime(row[1], '%d/%m/%y, %H:%M:%S'))
                                self.TimeList2.append(Time2)
                                #print(Time2)


    def update_frame(self):
        print('ss')

        if self.NameLabe.text()!='stop':
            ret, self.image = self.capture.read()
            self.displayImage(self.image, self.encode_list, self.class_names, 1)
        else:
            self.capture = cv2.VideoCapture(int(1), cv2.CAP_DSHOW)
            self.timer.start(10000)
            print(cv2.VideoCapture(int(1), cv2.CAP_DSHOW))

    def displayImage(self, image, encode_list, class_names, window=1):
        """
        :param image: frame from camera
        :param encode_list: known face encoding list
        :param class_names: known face names
        :param window: number of window
        :return:
        """

        image = cv2.resize(image, (640, 480))
        try:
            image = self.face_rec_(image, encode_list, class_names)
        except Exception as e:
            print(e)
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        outImage = outImage.rgbSwapped()
        if window == 1:

                self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
                self.imgLabel.setScaledContents(True)

