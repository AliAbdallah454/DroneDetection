from math import floor, ceil
import cv2
from cvzone.FaceDetectionModule import FaceDetector
import pyfirmata2 as p

from sklearn.linear_model import LinearRegression

import threading
import cvzone

from sklearn.linear_model import LinearRegression



board = p.Arduino("COM10")
servo_x = board.get_pin("d:8:s")
servo_y = board.get_pin("d:10:s")
laser = board.get_pin("d:7:o")

laser.write(1)

servo_x.write(90)
servo_y.write(90)

cap = cv2.VideoCapture(0)

detector = FaceDetector(minDetectionCon=0.5)
prev = 0
x_angle = 90
y_angle = 85
turn = x_angle

up = 1

while True:
    success, img = cap.read()
    
    img = cv2.resize(img, (640, 640))
    img = cv2.flip(img, 1)

    img, boxes = detector.findFaces(img)


    if boxes:
        (x, y) = boxes[0]["center"]

        y  = y / 640

        # r = int(input(">> "))
        # if x <= 1/2:
        #     x_angle = x_coef1 * x + x_intercept1 - 5
        # elif 1/2 < x:
        #     x_angle = x_coef2 * x + x_intercept2 + 2
            
        # servo_y.write(r)

        y_angle = 63.333 * y + 57.444

        # y_angle = 85
        # x_ang = ceil(x_angle)
        # y_ang = ceil(y_angle)
        # servo_x.write(x_ang)
        servo_y.write(y_angle)

        # print(f"{x} : {x_ang}")

        cvzone.putTextRect(img, f'{y}', (30, 30))

    cv2.imshow("Image", img)

    if cv2.waitKey(1) == ord('q'):
        break

servo_x.write(90)
servo_y.write(85)
cv2.destroyAllWindows()