# Forklift AI Distance Alert — AI Forklift Safety System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.9-green)](https://google.github.io/mediapipe/)

**Forklift AI Distance Alert is an open-source forklift safety system that uses computer vision to detect nearby people and estimate their distance using a standard camera.**

Built with Python, OpenCV, and MediaPipe, the application provides real-time visual proximity warnings without requiring cloud processing or specialized distance sensors. It is designed as an experimental safety-assistance tool for forklifts, warehouses, industrial environments, and computer vision research.

## Demo

[![Forklift AI pedestrian detection and distance alert demo](https://img.youtube.com/vi/4yzkxopYLfU/0.jpg)](https://youtu.be/4yzkxopYLfU?si=RwTlUTyH8V1htSgQ)

Watch the demo to see real-time human detection, distance estimation, and proximity alerts in action.

## Features

- **Real-time human detection** using Google MediaPipe
- **Camera-based distance estimation** using detected body height and camera calibration
- **Three-level proximity warning system**
  - 🔴 **Danger:** person detected closer than 0.5 m
  - 🟡 **Caution:** person detected between 0.5 m and 1 m
  - 🟢 **Safe:** detected distance greater than 1 m
- **Fullscreen camera display** suitable for an operator-facing screen
- **Offline processing** with no cloud connection required
- **CPU-based operation** without requiring a dedicated GPU
- **Standard webcam support**
- Adjustable camera calibration parameters

## Use Cases

Forklift AI Distance Alert can be used as a prototype or research platform for:

- Forklift pedestrian detection
- Forklift proximity warning systems
- Warehouse pedestrian safety experiments
- Forklift blind-spot monitoring
- Computer vision collision-warning research
- Industrial human detection prototypes
- Camera-based distance estimation experiments
- Raspberry Pi or laptop-based forklift safety projects

> **Important:** This project is a safety-assistance prototype and should not be treated as a certified industrial safety system or as a replacement for trained operators, approved safety equipment, or required workplace safety procedures.

## Installation

### Requirements

- Python 3.8+
- Webcam or compatible camera
- `pip`

### Clone the Repository

```bash
git clone https://github.com/Amirmobash/ForkliftAIDistanceAlert.git
cd ForkliftAIDistanceAlert
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

The project uses:

- OpenCV
- MediaPipe
- NumPy

## Quick Start

Run the application with:

```bash
python main.py
```

The application opens the camera feed in fullscreen mode and displays proximity alert bars based on the estimated distance to detected people.

Press `ESC` or `q` to exit.

## How the Forklift Pedestrian Detection System Works

The system follows a simple computer vision pipeline:

1. A camera captures live video near the forklift.
2. MediaPipe processes the video to detect human body landmarks.
3. The application uses the detected body dimensions and camera calibration to estimate distance.
4. The estimated distance is compared with configured safety thresholds.
5. A visual warning is displayed to the operator.

The default warning zones are:

| Estimated Distance | Alert | Meaning |
|---|---|---|
| `< 0.5 m` | 🔴 Red | Danger |
| `0.5–1 m` | 🟡 Yellow | Caution |
| `> 1 m` | 🟢 Green | Safe |

This approach allows the prototype to perform pedestrian proximity detection using a conventional camera rather than a dedicated distance sensor.

## Configuration and Camera Calibration

Distance estimation depends on camera calibration and an assumed reference human height.

The default reference height is:

```text
1.7 m
```

To adapt the system to a different camera or installation position, adjust the following parameters in `main.py`:

```python
KNOWN_HEIGHT
FOCAL_LENGTH
```

Accurate calibration is important because camera characteristics, mounting position, perspective, human height, and environmental conditions can affect distance estimates.

## Project Structure

```text
ForkliftAIDistanceAlert/
├── README.md
├── requirements.txt
├── main.py
├── assets/
│   └── preview.png
└── LICENSE
```

### `main.py`

Contains the main application logic for camera capture, human detection, distance estimation, and visual alerts.

### `requirements.txt`

Contains the Python dependencies required to run the application.

### `assets/`

Contains optional images or screenshots used by the project documentation.

## Tech Stack

- **Python** — application logic
- **OpenCV** — camera capture and image processing
- **MediaPipe** — human body landmark detection
- **NumPy** — numerical operations

## Limitations and Safety Considerations

Forklift AI Distance Alert estimates distance from camera imagery. It does not directly measure physical distance with LiDAR, radar, ultrasonic sensors, or other dedicated ranging hardware.

Accuracy can therefore be affected by factors including:

- Camera calibration
- Camera angle and mounting position
- Person height
- Partial body visibility
- Occlusion
- Lighting conditions
- Image quality
- Detection reliability

The configured distance thresholds should not be interpreted as certified safety distances.

For real industrial deployment, appropriate risk assessment, testing, redundancy, and compliance with applicable workplace and machinery safety requirements are necessary.

## FAQ

### Can a webcam detect pedestrians around a forklift?

This project demonstrates camera-based human detection using MediaPipe. A standard camera provides the video stream, while the software identifies human body landmarks and estimates proximity.

### Does Forklift AI Distance Alert require internet access?

No. Detection and distance estimation are performed locally, so the application does not require a cloud service during normal operation.

### Does the system require a GPU?

The current implementation is designed to run on CPU and does not require a dedicated GPU.

### Can it run on a Raspberry Pi?

The application is intended to be lightweight enough for devices such as a Raspberry Pi or laptop, but actual performance depends on the Raspberry Pi model, camera, operating system, and MediaPipe/OpenCV compatibility.

### How does the system estimate the distance to a person?

Distance is estimated using detected human body dimensions, an assumed reference height, and the configured camera focal length.

### Is this a certified forklift collision avoidance system?

No. This repository is an experimental safety-assistance and computer vision project. It is not presented as a certified industrial collision-avoidance or personnel-protection system.

### Can I change the danger distance?

The distance logic is implemented in `main.py` and can be modified for experimentation. Any thresholds used in a real workplace should be determined through an appropriate safety assessment rather than relying on the defaults in this project.

## Contributing

Contributions, bug reports, and improvements are welcome.

To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test the changes.
5. Open a pull request describing what you changed.

Ideas for improvements may include detection reliability, calibration, performance optimization, documentation, and additional testing.

## Author

**Amir Mobasheraghdam**

- [GitHub — Amirmobash](https://github.com/Amirmobash)
- [Instagram — @amirmobasher.ir](https://instagram.com/amirmobasher.ir)

## License

This project is licensed under the [MIT License](LICENSE).

See the `LICENSE` file for the full license terms.

## Related Technologies

This project uses computer vision technologies commonly applied to real-time human detection and image processing:

- [MediaPipe](https://developers.google.com/mediapipe)
- [OpenCV](https://opencv.org/)
- [Python](https://www.python.org/)

If you are researching **forklift pedestrian detection**, **AI forklift safety**, **camera-based proximity warning**, or **computer vision for warehouse safety**, this repository provides a compact Python implementation for experimentation and further development.
