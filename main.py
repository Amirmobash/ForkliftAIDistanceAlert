"""
FactoryMind - Forklift & Pedestrian Safety Vision System
Developed by: Amir Mobasheraghdam
Version: 1.1
Date: 2026-04-06
License: MIT
Description: Real-time human detection and proximity alert using only a webcam.
             Visual side bars change color based on estimated distance:
             - Red   : Danger (< 0.5 m)
             - Yellow: Caution (0.5–1.0 m)
             - Green : Safe (> 1.0 m)
Powered by: MediaPipe + OpenCV
"""

import cv2
import mediapipe as mp

# ----------------------------------------------------------------------
# 1. CONFIGURATION & CALIBRATION
# ----------------------------------------------------------------------
# Calibration value (in pixels) representing a person standing ~1 meter away.
# Adjust this number based on your camera and desired sensitivity.
# Higher value = person needs to be taller (closer) to trigger red alert.
CALIBRATION_HEIGHT_PX = 400   # <-- change after real-world testing

# Alert thresholds (based on person height in pixels)
# Person appears taller when closer → higher pixel height = higher risk
RED_THRESHOLD = CALIBRATION_HEIGHT_PX          # >400 px → red (danger)
YELLOW_THRESHOLD = int(CALIBRATION_HEIGHT_PX * 0.6)  # >240 px → yellow

# Camera settings
CAMERA_ID = 0                     # 0 = built-in webcam, 1 = external
WINDOW_NAME = "FactoryMind"

# ----------------------------------------------------------------------
# 2. INITIALIZE MEDIAPIPE POSE
# ----------------------------------------------------------------------
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,           # 0,1,2 (higher = better but slower)
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# ----------------------------------------------------------------------
# 3. START WEBCAM & FULLSCREEN WINDOW
# ----------------------------------------------------------------------
cap = cv2.VideoCapture(CAMERA_ID)
if not cap.isOpened():
    print("❌ Error: Could not open webcam.")
    exit()

cv2.namedWindow(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

print("✅ FactoryMind started. Press 'q' to quit.")

# ----------------------------------------------------------------------
# 4. MAIN LOOP
# ----------------------------------------------------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Warning: Frame capture failed.")
        break

    # Mirror the view for intuitive left/right movement
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape

    # Convert BGR to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    # Default alert color = GREEN (safe)
    alert_color = (0, 255, 0)   # BGR format
    distance_status = "Safe (>1.0 m)"
    person_height_px = 0

    # ------------------------------------------------------------------
    # 5. HUMAN DETECTION & DISTANCE ESTIMATION
    # ------------------------------------------------------------------
    if results.pose_landmarks:
        # Draw pose skeleton on the frame
        mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
        )

        # Get all y-coordinates (vertical positions) of detected landmarks
        y_coords = [lm.y for lm in results.pose_landmarks.landmark]
        # Person height in pixels = (max_y - min_y) * frame_height
        person_height_px = (max(y_coords) - min(y_coords)) * height

        # Determine alert level based on pixel height
        if person_height_px > RED_THRESHOLD:
            alert_color = (0, 0, 255)          # RED
            distance_status = "DANGER (<0.5 m)"
        elif person_height_px > YELLOW_THRESHOLD:
            alert_color = (0, 255, 255)        # YELLOW
            distance_status = "CAUTION (0.5-1.0 m)"
        else:
            alert_color = (0, 255, 0)          # GREEN
            distance_status = "SAFE (>1.0 m)"

    # ------------------------------------------------------------------
    # 6. DRAW VISUAL ALERT BARS (left & right side)
    # ------------------------------------------------------------------
    bar_thickness = 40
    # Left bar
    cv2.rectangle(frame, (0, 0), (bar_thickness, height), alert_color, -1)
    # Right bar
    cv2.rectangle(frame, (width - bar_thickness, 0), (width, height), alert_color, -1)

    # ------------------------------------------------------------------
    # 7. DISPLAY TEXT INFO (optional, but helpful for debugging)
    # ------------------------------------------------------------------
    # Show current distance status on top-left corner
    cv2.putText(frame, distance_status, (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    # Show raw pixel height (for calibration)
    cv2.putText(frame, f"Height: {int(person_height_px)} px", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

    # Show author metadata on bottom-right
    cv2.putText(frame, "Amir Mobasheraghdam | FactoryMind", (width - 280, height - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

    # ------------------------------------------------------------------
    # 8. SHOW THE RESULT
    # ------------------------------------------------------------------
    cv2.imshow(WINDOW_NAME, frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ----------------------------------------------------------------------
# 9. CLEANUP
# ----------------------------------------------------------------------
cap.release()
cv2.destroyAllWindows()
print("👋 FactoryMind stopped.")
