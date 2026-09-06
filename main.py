"""
FactoryMind - Forklift & Pedestrian Safety Vision System

Real-time, single-person pose detection from a webcam with a visual proximity
indicator based on apparent person height in pixels.

IMPORTANT:
    This program does NOT measure physical distance directly. The configured
    distance labels are only estimates derived from camera-specific calibration.
    It must not be used as the sole safety control for industrial machinery.
"""

from __future__ import annotations

import argparse
import logging
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Final, Sequence

import cv2
import mediapipe as mp


LOGGER = logging.getLogger("factorymind")

WINDOW_NAME: Final[str] = "FactoryMind"
DEFAULT_CAMERA_ID: Final[int] = 0
DEFAULT_CALIBRATION_HEIGHT_PX: Final[float] = 400.0
DEFAULT_YELLOW_RATIO: Final[float] = 0.60
DEFAULT_MIN_VISIBILITY: Final[float] = 0.50
DEFAULT_HYSTERESIS_PX: Final[float] = 15.0
DEFAULT_BAR_THICKNESS_PX: Final[int] = 40

# OpenCV uses BGR color order.
COLOR_GREEN: Final[tuple[int, int, int]] = (0, 255, 0)
COLOR_YELLOW: Final[tuple[int, int, int]] = (0, 255, 255)
COLOR_RED: Final[tuple[int, int, int]] = (0, 0, 255)
COLOR_UNKNOWN: Final[tuple[int, int, int]] = (128, 128, 128)
COLOR_WHITE: Final[tuple[int, int, int]] = (255, 255, 255)
COLOR_LIGHT_GRAY: Final[tuple[int, int, int]] = (200, 200, 200)


class AlertLevel(Enum):
    UNKNOWN = "UNKNOWN"
    SAFE = "SAFE"
    CAUTION = "CAUTION"
    DANGER = "DANGER"


@dataclass(frozen=True)
class Config:
    camera_id: int = DEFAULT_CAMERA_ID
    calibration_height_px: float = DEFAULT_CALIBRATION_HEIGHT_PX
    yellow_ratio: float = DEFAULT_YELLOW_RATIO
    min_visibility: float = DEFAULT_MIN_VISIBILITY
    hysteresis_px: float = DEFAULT_HYSTERESIS_PX
    model_complexity: int = 1
    min_detection_confidence: float = 0.5
    min_tracking_confidence: float = 0.5
    fullscreen: bool = True

    @property
    def red_threshold_px(self) -> float:
        return self.calibration_height_px

    @property
    def yellow_threshold_px(self) -> float:
        return self.calibration_height_px * self.yellow_ratio

    def validate(self) -> None:
        if self.camera_id < 0:
            raise ValueError("camera_id must be >= 0")
        if self.calibration_height_px <= 0:
            raise ValueError("calibration_height_px must be > 0")
        if not 0.0 < self.yellow_ratio < 1.0:
            raise ValueError("yellow_ratio must be between 0 and 1")
        if not 0.0 <= self.min_visibility <= 1.0:
            raise ValueError("min_visibility must be between 0 and 1")
        if self.hysteresis_px < 0:
            raise ValueError("hysteresis_px must be >= 0")
        if self.model_complexity not in (0, 1, 2):
            raise ValueError("model_complexity must be 0, 1, or 2")
        for name, value in (
            ("min_detection_confidence", self.min_detection_confidence),
            ("min_tracking_confidence", self.min_tracking_confidence),
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0 and 1")


@dataclass(frozen=True)
class Detection:
    person_height_px: float | None
    alert_level: AlertLevel


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "FactoryMind webcam pose monitor. Distance labels are calibrated "
            "estimates, not direct physical measurements."
        )
    )
    parser.add_argument("--camera", type=int, default=DEFAULT_CAMERA_ID)
    parser.add_argument(
        "--calibration-height",
        type=float,
        default=DEFAULT_CALIBRATION_HEIGHT_PX,
        help="Apparent person height in pixels used as the danger threshold.",
    )
    parser.add_argument(
        "--yellow-ratio",
        type=float,
        default=DEFAULT_YELLOW_RATIO,
        help="Caution threshold as a fraction of the danger threshold.",
    )
    parser.add_argument(
        "--min-visibility",
        type=float,
        default=DEFAULT_MIN_VISIBILITY,
        help="Minimum MediaPipe landmark visibility used for height estimation.",
    )
    parser.add_argument(
        "--hysteresis",
        type=float,
        default=DEFAULT_HYSTERESIS_PX,
        help="Pixel hysteresis used to reduce alert-state flicker.",
    )
    parser.add_argument(
        "--windowed",
        action="store_true",
        help="Run in a resizable window instead of fullscreen.",
    )
    parser.add_argument("--log-level", choices=("DEBUG", "INFO", "WARNING", "ERROR"), default="INFO")
    return parser


def estimate_person_height_px(landmarks: Sequence[object], frame_height: int, min_visibility: float) -> float | None:
    """Estimate visible person height from normalized MediaPipe landmark Y positions."""
    if frame_height <= 0:
        return None

    visible_y: list[float] = []
    for landmark in landmarks:
        visibility = float(getattr(landmark, "visibility", 1.0))
        y = float(getattr(landmark, "y"))
        if visibility >= min_visibility:
            # Pose landmarks can briefly extend outside the normalized image.
            visible_y.append(min(1.0, max(0.0, y)))

    # A tiny subset of landmarks is not a reliable whole-body height estimate.
    if len(visible_y) < 4:
        return None

    height_px = (max(visible_y) - min(visible_y)) * frame_height
    return height_px if height_px > 0.0 else None


def classify_alert(
    person_height_px: float | None,
    previous: AlertLevel,
    yellow_threshold_px: float,
    red_threshold_px: float,
    hysteresis_px: float,
) -> AlertLevel:
    """Classify apparent proximity with hysteresis around state boundaries."""
    if person_height_px is None:
        return AlertLevel.UNKNOWN

    if previous is AlertLevel.DANGER and person_height_px >= red_threshold_px - hysteresis_px:
        return AlertLevel.DANGER
    if previous is AlertLevel.CAUTION:
        if person_height_px >= red_threshold_px + hysteresis_px:
            return AlertLevel.DANGER
        if person_height_px >= yellow_threshold_px - hysteresis_px:
            return AlertLevel.CAUTION
    if previous is AlertLevel.SAFE and person_height_px <= yellow_threshold_px + hysteresis_px:
        return AlertLevel.SAFE

    if person_height_px >= red_threshold_px:
        return AlertLevel.DANGER
    if person_height_px >= yellow_threshold_px:
        return AlertLevel.CAUTION
    return AlertLevel.SAFE


def alert_color(level: AlertLevel) -> tuple[int, int, int]:
    return {
        AlertLevel.UNKNOWN: COLOR_UNKNOWN,
        AlertLevel.SAFE: COLOR_GREEN,
        AlertLevel.CAUTION: COLOR_YELLOW,
        AlertLevel.DANGER: COLOR_RED,
    }[level]


def alert_text(level: AlertLevel) -> str:
    return {
        AlertLevel.UNKNOWN: "NO RELIABLE PERSON DETECTION",
        AlertLevel.SAFE: "SAFE (calibrated estimate >1.0 m)",
        AlertLevel.CAUTION: "CAUTION (calibrated estimate 0.5-1.0 m)",
        AlertLevel.DANGER: "DANGER (calibrated estimate <0.5 m)",
    }[level]


def configure_window(fullscreen: bool) -> None:
    flag = cv2.WINDOW_NORMAL if not fullscreen else cv2.WINDOW_NORMAL
    cv2.namedWindow(WINDOW_NAME, flag)
    if fullscreen:
        try:
            cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        except cv2.error as exc:
            LOGGER.warning("Fullscreen mode unavailable: %s", exc)


def draw_overlay(frame, detection: Detection) -> None:
    height, width = frame.shape[:2]
    color = alert_color(detection.alert_level)
    bar = min(DEFAULT_BAR_THICKNESS_PX, max(1, width // 5))

    cv2.rectangle(frame, (0, 0), (bar, height), color, -1)
    cv2.rectangle(frame, (max(0, width - bar), 0), (width, height), color, -1)

    text_x = min(width - 1, bar + 10)
    cv2.putText(
        frame,
        alert_text(detection.alert_level),
        (text_x, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        COLOR_WHITE,
        2,
        cv2.LINE_AA,
    )

    height_text = (
        "Height: unavailable"
        if detection.person_height_px is None
        else f"Height: {detection.person_height_px:.0f} px"
    )
    cv2.putText(
        frame,
        height_text,
        (text_x, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        COLOR_LIGHT_GRAY,
        1,
        cv2.LINE_AA,
    )

    footer = "FactoryMind | q/ESC: quit"
    (footer_width, footer_height), _ = cv2.getTextSize(footer, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    footer_x = max(bar + 5, width - bar - footer_width - 10)
    footer_y = max(footer_height + 5, height - 15)
    cv2.putText(
        frame,
        footer,
        (footer_x, footer_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        COLOR_LIGHT_GRAY,
        1,
        cv2.LINE_AA,
    )


def run(config: Config) -> int:
    config.validate()

    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    capture = cv2.VideoCapture(config.camera_id)
    if not capture.isOpened():
        LOGGER.error("Could not open camera %d.", config.camera_id)
        capture.release()
        return 2

    pose = mp_pose.Pose(
        static_image_mode=False,
        model_complexity=config.model_complexity,
        min_detection_confidence=config.min_detection_confidence,
        min_tracking_confidence=config.min_tracking_confidence,
    )

    previous_level = AlertLevel.UNKNOWN

    try:
        configure_window(config.fullscreen)
        LOGGER.info("FactoryMind started. Press q or ESC to quit.")
        LOGGER.warning(
            "Distance labels are camera-calibrated estimates only; this software is not a certified safety device."
        )

        while True:
            ok, frame = capture.read()
            if not ok or frame is None:
                LOGGER.error("Camera frame capture failed.")
                return 3

            frame = cv2.flip(frame, 1)
            frame_height = frame.shape[0]
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb_frame.flags.writeable = False
            results = pose.process(rgb_frame)

            person_height_px: float | None = None
            if results.pose_landmarks:
                person_height_px = estimate_person_height_px(
                    results.pose_landmarks.landmark,
                    frame_height,
                    config.min_visibility,
                )
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            level = classify_alert(
                person_height_px,
                previous_level,
                config.yellow_threshold_px,
                config.red_threshold_px,
                config.hysteresis_px,
            )
            previous_level = level
            detection = Detection(person_height_px=person_height_px, alert_level=level)

            draw_overlay(frame, detection)
            cv2.imshow(WINDOW_NAME, frame)

            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):
                return 0

    except KeyboardInterrupt:
        LOGGER.info("Interrupted by user.")
        return 0
    except cv2.error:
        LOGGER.exception("OpenCV runtime error.")
        return 4
    finally:
        capture.release()
        pose.close()
        cv2.destroyAllWindows()
        LOGGER.info("FactoryMind stopped.")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    config = Config(
        camera_id=args.camera,
        calibration_height_px=args.calibration_height,
        yellow_ratio=args.yellow_ratio,
        min_visibility=args.min_visibility,
        hysteresis_px=args.hysteresis,
        fullscreen=not args.windowed,
    )

    try:
        return run(config)
    except ValueError as exc:
        LOGGER.error("Invalid configuration: %s", exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
