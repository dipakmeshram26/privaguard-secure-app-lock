"""
Webcam Intruder Capture Module for AppLocker.
Silently captures a photo when an intruder is detected.
Falls back gracefully if no camera is available.
"""
import os
import threading
from datetime import datetime


def _get_intruder_dir() -> str:
    """Returns path to the intruder photos directory."""
    local_app_data = os.environ.get("LOCALAPPDATA", os.path.expanduser("~"))
    intruder_dir = os.path.join(local_app_data, "PrivaGuard", "Intruders")
    if not os.path.exists(intruder_dir) and os.path.exists(os.path.join(local_app_data, "AppLocker", "Intruders")):
        intruder_dir = os.path.join(local_app_data, "AppLocker", "Intruders")
    os.makedirs(intruder_dir, exist_ok=True)
    return intruder_dir


def is_camera_available() -> bool:
    """Check if any webcam is connected and accessible using fast backend."""
    try:
        import cv2
        backend = cv2.CAP_DSHOW if os.name == 'nt' else cv2.CAP_ANY
        cap = cv2.VideoCapture(0, backend)
        available = cap.isOpened()
        cap.release()
        return available
    except Exception:
        return False


def capture_intruder_photo() -> str | None:
    """
    Silently and immediately capture a photo from the webcam.
    Uses DirectShow on Windows for instant (~1s) hardware initialization.
    Returns the saved file path on success, or None if capture failed.
    """
    try:
        import cv2
        backend = cv2.CAP_DSHOW if os.name == 'nt' else cv2.CAP_ANY
        cap = cv2.VideoCapture(0, backend)
        if not cap.isOpened():
            # Fallback to default backend if DirectShow is not supported
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                return None

        # Quick 1-frame buffer flush for clean sensor auto-exposure
        cap.read()
        ret, frame = cap.read()
        cap.release()

        if not ret or frame is None:
            return None

        # Save the photo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"intruder_{timestamp}.jpg"
        filepath = os.path.join(_get_intruder_dir(), filename)
        cv2.imwrite(filepath, frame)

        return filepath if os.path.exists(filepath) else None

    except Exception as e:
        print(f"[WebcamCapture] Error: {e}")
        return None


def capture_async(callback=None):
    """
    Capture photo in background thread.
    callback(photo_path_or_None) is called when done.
    """
    def _do():
        path = capture_intruder_photo()
        if callback:
            callback(path)

    threading.Thread(target=_do, daemon=True).start()


def get_all_intruder_photos() -> list:
    """Return list of all saved intruder photos (sorted newest first)."""
    intruder_dir = _get_intruder_dir()
    try:
        files = [
            os.path.join(intruder_dir, f)
            for f in os.listdir(intruder_dir)
            if f.endswith(".jpg") or f.endswith(".png")
        ]
        return sorted(files, key=os.path.getmtime, reverse=True)
    except Exception:
        return []
