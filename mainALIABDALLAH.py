from math import ceil, floor
import cv2
from cvzone.FaceDetectionModule import FaceDetector
import pyfirmata2 as p
############################################


def draw_cross(frame):
    height, width, _ = frame.shape
    center_x, center_y = width // 2, height // 2
    # Draw vertical line
    cv2.line(frame, (center_x, 0), (center_x, height), (0, 0, 255), 3)
    # Draw horizontal line
    cv2.line(frame, (0, center_y), (width, center_y), (0, 0, 255), 3)
    return frame


############################################
# x coef
x_coef_left = 101.15758028
x_intercept_left = 40.51306945

x_coef_right = 95.16393443
x_intercept_right = 41.71311475

# # y coef
y_coef_up = 110
y_intercept_up = 23

y_coef_down = 66.66666667
y_intercept_down = 51.16666667


board = p.Arduino("COM10")
servo_x = board.get_pin("d:8:s")
servo_y = board.get_pin("d:10:s")
laser1 = board.get_pin("d:7:o")

servo_x.write(90)
servo_y.write(90)

cap = cv2.VideoCapture(0)

detector = FaceDetector(minDetectionCon=0.7)

x_angle = 90
y_angle = 84

x_ang = x_angle
y_ang = y_angle

turn = x_angle

prev_face = None

while True:
    success, img = cap.read()

    img = cv2.resize(img, (640, 640))
    img = cv2.flip(img, 1)

    img, boxes = detector.findFaces(img)

    if boxes:
        laser1.write(1)
        (x, y) = boxes[0]["center"]

        x = x / 640
        y = y / 640

        # down left
        if 1/2 < y <= 0.85 and x <= 0.2:
            x_angle = x_coef_left * x + x_intercept_left + 2
            y_angle = y_coef_down * y + y_intercept_down - 2
        elif 1 / 2 < y <= 0.85 and 0.2 < x <= 1/2:
            x_angle = x_coef_left * x + x_intercept_left
            y_angle = y_coef_down * y + y_intercept_down
        elif 0.85 < y < 1 and 0.2 < x <= 1/2:
            x_angle = x_coef_left * x + x_intercept_left
            y_angle = y_coef_down * y + y_intercept_down - 2
        elif 0.85 < y and x <= 0.2:
            x_angle = x_coef_left * x + x_intercept_left + 4
            y_angle = y_coef_down * y + y_intercept_down - 2
        # down right
        elif 1/2 < y and 1/2 < x:
            x_angle = x_coef_right * x + x_intercept_right - 3
            y_angle = y_coef_down * y + y_intercept_down - 2
        # up left
        elif y <= 1/2 and 0.2 < x <= 1/2:
            x_angle = x_coef_left * x + x_intercept_left - 8
            y_angle = y_coef_up * y + y_intercept_up
        elif 0.2 <= y <= 1/2 and x <= 0.2:
            x_angle = x_coef_left * x + x_intercept_left - 2
            y_angle = y_coef_up * y + y_intercept_up
        elif y <= 0.2 and x <= 0.2:
            x_angle = x_coef_left * x + x_intercept_left - 7
            y_angle = y_coef_up * y + y_intercept_up
        # up right
        elif 0.2 < y <= 1/2 and 1/2 < x:
            x_angle = x_coef_right * x + x_intercept_right - 5
            y_angle = y_coef_up * y + y_intercept_up
        elif y < 0.2 and 1 / 2 < x <= 0.8:
            x_angle = x_coef_right * x + x_intercept_right - 5
            y_angle = y_coef_up * y + y_intercept_up + 3
        elif y < 0.2 and 0.8 < x < 1:
            x_angle = x_coef_right * x + x_intercept_right - 5
            y_angle = y_coef_up * y + y_intercept_up + 3

        if y <= 1/2:
            x_ang = ceil(x_angle)
            y_ang = ceil(y_angle)
        elif y > 1/2:
            x_ang = floor(x_angle)
            y_ang = floor(y_angle)

        if prev_face is None:
            servo_x.write(x_ang)
            servo_y.write(y_ang)
            prev_face = (x_ang, y_ang)
        else:
            if abs(prev_face[0] - x_ang) < 10 and abs(prev_face[1] - y_ang) < 10:
                servo_x.write(x_ang)
                servo_y.write(y_ang)
                prev_face = (x_ang, y_ang)

        print(f"{y}: {y_ang}")

    else:
        prev_face = None
        laser1.write(0)

    # cv2.imshow("Image", img)
    frame_with_cross = draw_cross(img.copy())
    cv2.imshow('Frame with Cross', frame_with_cross)

    if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == ord('Q'):
        break

servo_x.write(90)
servo_y.write(84)
laser1.write(0)
cv2.destroyAllWindows()
