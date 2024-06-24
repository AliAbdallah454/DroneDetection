import cv2
import os

save_dir = "c1"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open the camera.")
    exit()

frame_counter = 0

i = 0
with open("number.txt", 'r') as file:
    n = int(file.readline())
    i = n

while True:
    ret, frame = cap.read()

    if ret:
        cv2.imshow('Camera', frame)

        frame_counter += 1
        if frame_counter % 30 == 0:
            img_name = os.path.join(save_dir, f"c1_{i}.jpg")
            cv2.imwrite(img_name, frame)
        i += 1
        with open("number.txt", 'w') as file:
            file.write(str(i))
        

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("Error: Could not read the frame.")
        break

cap.release()
cv2.destroyAllWindows()