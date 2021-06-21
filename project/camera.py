import numpy as np
import cv2 as cv
import cv2
import datetime


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


print(cap.get(3))
print(cap.get(4))

while cap.isOpened():
    ret, frame = cap.read()
    if ret == True:
        font = cv2.FONT_HERSHEY_SIMPLEX

        # data
        date = str(datetime.datetime.now())
        cv2.putText(frame, date, (10, 66), font, 0.5, (0, 255, 255), 1, cv2.LINE_AA)

        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('cqq', frame)  # gray

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()