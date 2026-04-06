# Forklift AI Distance Alert 🚧

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.9-green)](https://google.github.io/mediapipe/)

**An AI-powered safety assistant for forklifts that detects nearby humans using only a standard webcam.**  
Real-time, offline, and lightweight – designed to prevent accidents in industrial environments.

---

## 🎥 Demo

[![Watch the demo on YouTube](https://img.youtube.com/vi/4yzkxopYLfU/0.jpg)](https://youtu.be/4yzkxopYLfU?si=RwTlUTyH8V1htSgQ)

Click the image above to see Forklift AI Distance Alert in action.

---

## 🚀 Features

- ✅ **Real‑time human detection** using Google MediaPipe  
- 📏 **Distance estimation** based on body height and camera calibration  
- 🎨 **Visual side‑bar alerts** with color coding:
  - 🔴 **Red** – Danger (< 0.5 m)
  - 🟡 **Yellow** – Caution (0.5 m – 1 m)
  - 🟢 **Green** – Safe (> 1 m)
- 🖥️ **Fullscreen display** for clear visibility on forklift dashboards  
- 📴 **Offline & lightweight** – no internet required, runs on CPU

---

## 🎯 How It Works

The tool runs on a device (e.g., Raspberry Pi, laptop) mounted to the back of a forklift.  
It captures live video, detects humans, estimates their distance, and draws side bars on the screen:

- **Red bar** appears when a person is closer than 0.5 m – immediate danger  
- **Yellow bar** for 0.5–1 m – caution zone  
- **Green bar** for distances above 1 m – safe  

These visual alerts help operators react quickly, reducing back‑over and blind‑spot accidents.

---

## 🛠️ Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/Amirmobash/ForkliftAIDistanceAlert.git
   cd ForkliftAIDistanceAlert
   ```

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

   `requirements.txt` should contain:
   ```
   opencv-python
   mediapipe
   numpy
   ```

---

## ▶️ Run the Application

```bash
python main.py
```

Press `ESC` or `q` to exit. The app will open a fullscreen window showing the camera feed with distance alert bars.

---

## 🧠 Customisation & Calibration

Distance estimation uses a reference human height (default 1.7 m).  
To calibrate for your camera and environment, adjust the `KNOWN_HEIGHT` and `FOCAL_LENGTH` parameters inside `main.py`.

---

## 📂 Project Structure

```
ForkliftAIDistanceAlert/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── main.py                # Main application (LiftSafe engine)
├── assets/
│   └── preview.png        # Optional screenshot
└── LICENSE                # MIT License
```

---

## 👨‍💻 Author

**Amir Mobasher**  
- 📸 [Instagram @amirmobasher.ir](https://instagram.com/amirmobasher.ir)  
- 🌐 [GitHub Amirmobash](https://github.com/Amirmobash)

---

## 📄 License

This project is licensed under the **MIT License** – free for personal and industrial use.  
Attribution is appreciated 🙏

---

## 🌟 SEO Keywords

*forklift safety, AI human detection, distance alert, MediaPipe, computer vision, industrial safety, collision avoidance, blind spot detection, real‑time monitoring, opencv forklift assistant*

```

### What was corrected / improved:

- **Video integration** – Clickable YouTube thumbnail that plays the demo.
- **SEO keywords** – Added a visible keyword list at the end for better search engine indexing.
- **Clearer structure** – Proper headings, badges, and consistent naming.
- **Grammar & typos** – Fixed broken sentences and capitalisation.
- **License line** – Changed from `LICENSE mit Amir Mobasheraghdam` to standard MIT mention.
- **Installation details** – Explicit `requirements.txt` content.
- **Calibration hint** – Brief note for customisation.
- **Fullscreen and exit keys** – Added for usability.

