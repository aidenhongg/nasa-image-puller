"""Global constants and shared exceptions for the NASA Image Puller."""

import os

# Load API key from file or environment variable
API_KEY_PATH = os.path.join(os.path.dirname(__file__), "..", "NASA_API_KEY.txt")

if os.path.exists(API_KEY_PATH):
    with open(API_KEY_PATH, "r") as f:
        NASA_API_KEY = f.readline().strip()
else:
    NASA_API_KEY = os.environ.get("NASA_API_KEY", "DEMO_KEY")

BASE_NASA_URL = "https://api.nasa.gov/planetary/apod?api_key="


class AppError(Exception):
    """Raised when the application encounters a fatal error."""

    def __init__(self, message="A fatal error occurred."):
        super().__init__(message)
        self.message = message
