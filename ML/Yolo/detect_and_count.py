from ultralytics import YOLO
import cv2, csv
from datetime import datetime, timedelta

# Load the pre-trained YOLOv8 model
model = YOLO("yolov8n.pt")

# Path to your video file
video_path = "videos/traffic_footage.mp4"
cap = cv2.VideoCapture(video_path)

# Check if video loaded correctly
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Get the video's FPS; if unavailable, assume 30 fps
fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0:
    fps = 30

# For testing with a short video, use 10-second intervals.
interval_seconds = 10
frame_threshold = int(fps * interval_seconds)

results_data = []
junction = 1
start_time = datetime(2015, 11, 1, 0, 0, 0)
frame_count = 0
vehicle_count = 0

print("Processing video...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Reached end of video.")
        break

    frame_count += 1

    # Run detection every 30 frames (approximately once per second at 30 fps)
    if frame_count % 30 == 0:
        result = model(frame)[0]
        # Count vehicles if the detected object is one of the desired classes
        vehicle_count += sum(
            1 for c in result.boxes.cls.tolist()
            if model.names[int(c)] in ['car', 'bus', 'truck', 'motorbike']
        )

    # Once we've processed enough frames for the interval, save the results
    if frame_count >= frame_threshold:
        row_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        row_id = f"{start_time.strftime('%Y%m%d%H%M%S')}{junction}"
        results_data.append([row_time, junction, vehicle_count, row_id])
        print(f"Interval ending at {row_time}: {vehicle_count} vehicles detected.")
        # Reset counts and increment time for the next interval
        start_time += timedelta(seconds=interval_seconds)
        vehicle_count = 0
        frame_count = 0

# If there are any leftover frames (a partial interval), output those too
if frame_count > 0:
    row_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
    row_id = f"{start_time.strftime('%Y%m%d%H%M%S')}{junction}"
    results_data.append([row_time, junction, vehicle_count, row_id])
    print(f"Final interval ending at {row_time}: {vehicle_count} vehicles detected.")

cap.release()

# Save results to CSV in the "output" folder
with open("output/traffic_report.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["DateTime", "Junction", "Vehicles", "ID"])
    writer.writerows(results_data)

print("CSV file saved in output/traffic_report.csv")
