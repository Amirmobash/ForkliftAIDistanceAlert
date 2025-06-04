# ForkliftAIDistanceAlert 🚧

**An AI-powered safety assistant for forklifts that detects nearby humans using only a webcam.**

---

## 🚀 Features

- Real-time human detection using [MediaPipe](https://google.github.io/mediapipe/)
- Distance estimation based on body size and camera calibration
- Visual side bars indicating proximity with color-coded alerts:
  - 🔴 Red = Danger (< 0.5m)
  - 🟡 Yellow = Caution (0.5m – 1m)
  - 🟢 Green = Safe (> 1m)
- Fullscreen display for better visibility
- Offline & lightweight – no internet required

---

## 🎥 How It Works
This tool runs on a device mounted to the back of a forklift. It captures live video, detects human presence, and displays side alert bars:

- **Red**: Danger zone (closer than 0.5 meters)
- **Yellow**: Caution (between 0.5 and 1 meter)
- **Green**: Safe zone (greater than 1 meter)

These alerts help prevent accidents in industrial environments.

---

## 🛠️ Installation

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
python main.py
```

---

## 🖼 Preview

![Preview](assets/preview.png)

---

## 📂 Project Structure

```
ForkliftAIDistanceAlert/
├── README.md
├── requirements.txt
├── main.py              # Main application (LiftSafe)
├── assets/
│   └── preview.png      # Optional image or GIF for demonstration
└── LICENSE
```

---

## 👨‍💻 Author
Developed by **Amir Mobasher**  
📸 Instagram: [@amirmobasher.ir](https://instagram.com/amirmobasher.ir)  
🌐 GitHub: [Amirmobash](https://github.com/Amirmobash)

---

## 📄 License
MIT – free for personal and industrial use. Attribution appreciated 🙏
