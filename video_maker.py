from ultralytics import YOLO
import cv2
import cvzone
from math import ceil

model_name = "best_params"

model = YOLO(f"./runs/detect/{model_name}/weights/best.pt")

print("Launching video")
cap = cv2.VideoCapture('./test_videos/t1.mp4')

fps = cap.get(cv2.CAP_PROP_FPS)

output_video_path = './output_videos/output_video.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (640, 640))

while True:
    
    success, img = cap.read()

    img = cv2.resize(img, (640, 640))
    img = cv2.flip(img, 1)

    results = model(img, stream=True)

    for r in results:
        boxes = r.boxes
        for box in boxes:

            conf = ceil((box.conf[0] * 100)) / 100

            if conf < 0:
                continue
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cvzone.putTextRect(img, f'{conf}', (x1, y1 - 20))

    cv2.imshow("Image", img)
    out.write(img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()