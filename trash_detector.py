import cv2
from ultralytics import YOLO

# 1. Initialize model and video
model = YOLO("60_epochs_denoised.pt")
video_path = "v2.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("❌ Unable to open video")
    exit()

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# 2. Store detection results for each frame
results_by_frame = []

print("🚀 Analyzing video, please wait...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]  # Run YOLO model on the current frame
    frame_results = []

    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
        cls_id = int(box.cls[0])               # Class ID
        conf = float(box.conf[0])              # Confidence score
        label = model.names[cls_id]            # Class name

        frame_results.append({
            "label": label,
            "conf": conf,
            "box": (x1, y1, x2, y2)
        })

    results_by_frame.append({
        "frame": len(results_by_frame),
        "objects": frame_results
    })

cap.release()
print("✅ Analysis complete. Launching review UI...")

# 3. Display UI with trackbar and pause/play controls
cap = cv2.VideoCapture(video_path)
cv2.namedWindow("YOLO Review", cv2.WINDOW_NORMAL)

paused = False  # Flag to control pause/play state

def on_trackbar(val):
    """Callback function for trackbar."""
    global paused
    paused = True  # Automatically pause when user drags the trackbar
    cap.set(cv2.CAP_PROP_POS_FRAMES, val)

cv2.createTrackbar("Frame", "YOLO Review", 0, total_frames - 1, on_trackbar)

while True:
    if not paused:
        ret, frame = cap.read()
        if not ret:
            break
    else:
        # In paused state, manually fetch current frame
        frame_pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
        ret, frame = cap.read()
        if not ret:
            break

    frame_index = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

    # Draw bounding boxes for this frame
    if frame_index < len(results_by_frame):
        for obj in results_by_frame[frame_index]["objects"]:
            x1, y1, x2, y2 = obj["box"]
            label = obj["label"]
            conf = obj["conf"]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Update trackbar to reflect current frame
    cv2.setTrackbarPos("Frame", "YOLO Review", frame_index)
    cv2.imshow("YOLO Review", frame)

    key = cv2.waitKey(30) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('p'):  # Toggle pause/play when 'p' is pressed
        paused = not paused

cap.release()
cv2.destroyAllWindows()
