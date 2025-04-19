# ForkliftAIDistanceAlert 🚧

An AI-powered safety assistant that helps prevent accidents in industrial environments by detecting nearby humans and estimating their distance using a simple webcam.

## 🚀 Features

- Real-time human detection using MediaPipe
- Distance estimation based on body size and camera calibration
- Visual side bars (🔴 RED, 🟡 YELLOW, 🟢 GREEN) based on proximity
- Fullscreen display for better visibility
- Lightweight & offline – no internet connection required

## 🎥 How It Works

This tool is designed to be installed on the back of a forklift or other industrial vehicles. It continuously analyzes the video feed to detect humans and shows colored alert bars depending on how close a person is:

- **Red** = Danger (closer than 0.5m)  
- **Yellow** = Caution (0.5m to 1m)  
- **Green** = Safe (more than 1m away)

## 🛠️ Installation

```bash
pip install -r requirements.txt
▶️ Run the App
bash
Kopieren
Bearbeiten
python main.py
📷 Preview
(You can add an image or GIF here from the /media folder)

👨‍💻 Author
Developed by Amir Mobasher
📸 Instagram: @amirmobasher.ir
🌐 GitHub: github.com/Amirmobash

📄 License
MIT – free for personal and industrial use. Attribution appreciated 🙏
