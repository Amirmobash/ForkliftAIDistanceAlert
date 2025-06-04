import cv2
import mediapipe as mp

# راه‌اندازی MediaPipe برای تشخیص انسان
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# باز کردن وب‌کم
cap = cv2.VideoCapture(0)
cv2.namedWindow("FactoryMind", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("FactoryMind", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# ⚙️ تنظیمات کالیبراسیون دستی
calibration_height = 600  # این مقدار را تنظیم کن بر اساس تست
red_threshold = calibration_height      # خیلی نزدیک
yellow_threshold = calibration_height * 0.6  # نسبتاً نزدیک

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # معکوس کردن تصویر برای نمایش بهتر
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape

    # تشخیص وضعیت بدن
    results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    distance_color = (0, 255, 0)  # پیش‌فرض: سبز

    if results.pose_landmarks:
        # پیدا کردن مختصات شانه‌ها برای برآورد فاصله
        left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        # محاسبه ارتفاع فرضی بدن
        y_values = [lm.y for lm in results.pose_landmarks.landmark]
        min_y = min(y_values)
        max_y = max(y_values)
        person_height = (max_y - min_y) * height

        # رسم استخوان‌بندی بدن
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # بر اساس ارتفاع، فاصله فرضی را مشخص کن
        if person_height > red_threshold:
            distance_color = (0, 0, 255)  # قرمز = خیلی نزدیک
        elif person_height > yellow_threshold:
            distance_color = (0, 255, 255)  # زرد = متوسط
        else:
            distance_color = (0, 255, 0)  # سبز = دور

    # رسم نوارهای کناری
    bar_thickness = 40
    cv2.rectangle(frame, (0, 0), (bar_thickness, height), distance_color, -1)
    cv2.rectangle(frame, (width - bar_thickness, 0), (width, height), distance_color, -1)

    cv2.imshow("FactoryMind", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
