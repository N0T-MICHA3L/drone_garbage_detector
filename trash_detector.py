from roboflow import Roboflow
import supervision as sv
import cv2
import numpy as np

rf = Roboflow(api_key="1JmXCPJmKdbfUMh5FwbK")
project = rf.workspace().project("beach-garbage")
model = project.version(1).model



# 1. Initialize model and video
# model = YOLO("60_epochs_denoised.pt")
# video_path = "v2.mp4"
video_path = "dji_fly_20250713_155210_964_1752397003712_video.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("❌ Unable to open video")
    exit()

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# 2. Store detection results for each frame
results_by_frame = []

print("🚀 Analyzing video, please wait...")
# cv2.namedWindow("Review", cv2.WINDOW_NORMAL)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.predict(frame).json()
    # Convert Roboflow results to supervision Detections format
    detections_list = results.get("predictions", [])
    xyxy = []
    confidences = []
    class_names = []
    for det in detections_list:
        x1 = int(det["x"] - det["width"] / 2)
        y1 = int(det["y"] - det["height"] / 2)
        x2 = int(det["x"] + det["width"] / 2)
        y2 = int(det["y"] + det["height"] / 2)
        xyxy.append([x1, y1, x2, y2])
        confidences.append(det["confidence"])
        class_names.append(det["class"])

    if len(xyxy) == 0:
        detections = sv.Detections(
            xyxy=np.zeros((0, 4), dtype=np.int32),
            confidence=np.zeros((0,), dtype=np.float32),
            class_id=np.zeros((0,), dtype=np.int32)
        )
    else:
        detections = sv.Detections(
            xyxy=np.array(xyxy, dtype=np.int32),
            confidence=np.array(confidences, dtype=np.float32),
            class_id=np.array([0]*len(class_names), dtype=np.int32)  # Or use a mapping if you have class IDs
        )

    label_annotator = sv.LabelAnnotator()
    bounding_box_annotator = sv.BoxAnnotator()
    frame = label_annotator.annotate(scene=frame, detections=detections)
    frame = bounding_box_annotator.annotate(scene=frame, detections=detections)

    frame_index = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    print(frame_index,'/', total_frames, ",", len(detections_list))
    # cv2.imwrite(f"output/frame_{frame_index}.jpg", frame)

    # # Store results in a compatible format for later display
    # frame_results = []
    # for i, box in enumerate(xyxy):
    #     frame_results.append({
    #         "label": class_names[i],
    #         "conf": confidences[i],
    #         "box": box
    #     })

    # results_by_frame.append({
    #     "frame": len(results_by_frame),
    #     "objects": frame_results
    # })

cap.release()
print("✅ Analysis complete. Launching review UI...")

# 3. Display UI with trackbar and pause/play controls
# cap = cv2.VideoCapture(video_path)
# cv2.namedWindow("YOLO Review", cv2.WINDOW_NORMAL)

# paused = False  # Flag to control pause/play state

# def on_trackbar(val):
#     """Callback function for trackbar."""
#     global paused
#     paused = True  # Automatically pause when user drags the trackbar
#     cap.set(cv2.CAP_PROP_POS_FRAMES, val)

# cv2.createTrackbar("Frame", "YOLO Review", 0, total_frames - 1, on_trackbar)

# while True:
#     if not paused:
#         ret, frame = cap.read()
#         if not ret:
#             break
#     else:
#         # In paused state, manually fetch current frame
#         frame_pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
#         cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
#         ret, frame = cap.read()
#         if not ret:
#             break

#     frame_index = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

#     # Draw bounding boxes for this frame
#     # if frame_index < len(results_by_frame):
#     #     for obj in results_by_frame[frame_index]["objects"]:
#     #         x1, y1, x2, y2 = obj["box"]
#     #         label = obj["label"]
#     #         conf = obj["conf"]
#     #         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#     #         cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
#     #                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

#     # Update trackbar to reflect current frame
#     cv2.setTrackbarPos("Frame", "YOLO Review", frame_index)
#     cv2.imshow("YOLO Review", frame)

#     key = cv2.waitKey(30) & 0xFF
#     if key == ord('q'):
#         break
#     elif key == ord('p'):  # Toggle pause/play when 'p' is pressed
#         paused = not paused

# cap.release()
cv2.destroyAllWindows()
