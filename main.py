from ultralytics import YOLO
import cv2
import cvzone
from math import ceil
import sys

from arduino_controller import arduino_controller

def calculate_angles(x, y):

    x_angle = ceil(91.66666667 * x + 40.277777777777786 + 2)
    y_angle = ceil(68.52425181 * y + 55.80254557963534)

    return x_angle, y_angle

def main():

    is_arduino_on = True if sys.argv[2] == "true" else False
    if is_arduino_on == False:
        print("Arduino Deactivated")
    else:
        print("Arduino Activated")

    if is_arduino_on == True:
        controller = arduino_controller("COM10", 8, 10, 7)
    threshold = 0
    try:
        threshold = float(sys.argv[1])
        print(f"Threshold of {threshold} will be used")
    except:
        print("Invalid Threshold, must be a number between 0 and 1")
        return

    prev_drone = None

    model_name = "drone_finetuning_1_sgd"
    model = YOLO(f"./runs/detect/{model_name}/weights/best.pt")

    # cap = cv2.VideoCapture("./vids/v1.mp4")
    cap = cv2.VideoCapture(0)

    cap.set(3, 640)  # Width
    cap.set(4, 640)  # Heigh

    while True:
        success, img = cap.read()

        img = cv2.resize(img, (640, 640))
        img = cv2.flip(img, 1)

        results = model(img, stream=True)

        for r in results:
            boxes = r.boxes
            for box in boxes:

                conf = ceil((box.conf[0] * 100)) / 100

                if conf < threshold:
                    continue

                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                x_middle = (x1 + x2) // 2
                y_middle = (y1 + y2) // 2

                y = y_middle / 640
                x = x_middle / 640

                x_angle, y_angle = calculate_angles(x, y)

                if is_arduino_on == True:
                    if prev_drone is None:
                        controller.move_servos(x_angle, y_angle)
                        prev_drone = (x_angle, y_angle)
                    else:
                        if abs(prev_drone[0] - x_angle) < 10 and abs(prev_drone[1] - y_angle) < 10:
                            controller.move_servos(x_angle, y_angle)
                            prev_drone = (x_angle, y_angle)

                print(x_angle, y_angle)

                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                cvzone.putTextRect(img, f'{conf}', (x1, y1 - 20))

            prev_drone = None

        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()