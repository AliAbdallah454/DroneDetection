from ultralytics import YOLO
import cv2
import cvzone
import os

model_name = "best_params"
model = YOLO(f"./runs/detect/{model_name}/weights/best.pt")

dir = "./ds/fod/test/images"

test_images = os.listdir(dir)
print(f"testing on {len(test_images)} images ...")

for image_path in test_images:

    image = cv2.imread(f"{dir}/{image_path}")
    results = model(image)
    for result in results:
        for bbox in result.boxes:
            x1, y1, x2, y2 = bbox.xyxy[0]
            confidence = bbox.conf[0]
            class_id = bbox.cls[0]
            label = model.names[int(class_id)]

            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 255), 3)
            cvzone.putTextRect(image, f'{confidence:.2f}', (int(x1), int(y1) - 20))

    resized_image = cv2.resize(image, (640, 640))

    cv2.imshow('Image', resized_image)
    cv2.waitKey(250)
cv2.destroyAllWindows()