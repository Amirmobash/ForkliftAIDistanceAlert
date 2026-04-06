"""
FactoryMind - Forklift & Pedestrian Safety Vision System
Developed by Amir Mobasheraghdam
Powered by MediaPipe + OpenCV
"""

import cv2
import mediapipe as mp

# Initialize MediaPipe Pose module
mp_pose = mp.solutions.pose
    distance_color = (0, 255, 0)

    if results.pose_landmarks:
        # Get shoulder landmarks to help estimate body scale
        left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        # Estimate vertical height of the person based on pose landmarks
        y_values = [lm.y for lm in results.pose_landmarks.landmark]
        person_height = (max(y_values) - min(y_values)) * height

        # Draw pose landmarks
        mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Determine color based on estimated proximity
        if person_height > red_threshold:
            distance_color = (0, 0, 255)      # Red = too close
        elif person_height > yellow_threshold:
            distance_color = (0, 255, 255)    # Yellow = medium
        else:
            distance_color = (0, 255, 0)      # Green = safe

    # Draw side proximity bars
    bar_thickness = 40
    cv2.rectangle(frame, (0, 0), (bar_thickness, height), distance_color, -1)
    cv2.rectangle(frame, (width - bar_thickness, 0), (width, height), distance_color, -1)

    # Show the result
    cv2.imshow("FactoryMind", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
