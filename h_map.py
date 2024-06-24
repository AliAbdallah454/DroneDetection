import cv2
from ultralytics import YOLO, solutions

model_name = "finetuning_1"

model = YOLO(f"./runs/detect/{model_name}/weights/best.pt")
cap = cv2.VideoCapture("vids/new_vid.mp4")

w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

video_writer = cv2.VideoWriter("heatmap_output.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

heatmap_obj = solutions.Heatmap(
    colormap=cv2.COLORMAP_PARULA,
    view_img=True,
    shape="circle",
    classes_names=model.names,
)

while cap.isOpened():
    success, im0 = cap.read()
    # im0 = cv2.resize(im0, (640, 640))   
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break
    tracks = model.track(im0, persist=True, show=False)

    im0 = heatmap_obj.generate_heatmap(im0, tracks)
    video_writer.write(im0)

cap.release()
video_writer.release()
cv2.destroyAllWindows()