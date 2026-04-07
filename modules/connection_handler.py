"""Handles HTTP connections to the NASA APOD API."""

import requests

from modules.globals import BASE_NASA_URL, NASA_API_KEY, AppError

MAX_RETRIES = 3
DEFAULT_START_DATE = "2024-01-01"
DEFAULT_END_DATE = "2024-01-31"


def build_url(start_date: str, end_date: str) -> str:
    """Build the NASA APOD API request URL from a date range."""
    if not start_date:
        start_date = DEFAULT_START_DATE
    if not end_date:
        end_date = DEFAULT_END_DATE

    return f"{BASE_NASA_URL}{NASA_API_KEY}&start_date={start_date}&end_date={end_date}"


def get_result(url: str) -> list[dict]:
    """Fetch APOD results from the NASA API. Retries up to MAX_RETRIES times."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            print(f"\nRequest failed (attempt {attempt}/{MAX_RETRIES}): HTTP {response.status_code}")
        except requests.RequestException:
            print(f"\nConnection failed (attempt {attempt}/{MAX_RETRIES}).")

    raise AppError("Failed to fetch results from NASA API after multiple attempts.")


def download_images(urls: tuple[str, str]) -> None:
    """Download two images from the given URLs and save as image1.jpg, image2.jpg."""
    if not urls[0] or not urls[1]:
        raise AppError("Not enough image URLs found for the given query.")

    for index, url in enumerate(urls, start=1):
        filename = f"image{index}.jpg"
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    with open(filename, "wb") as f:
                        f.write(response.content)
                    print(f"Saved {filename}")
                    break
                print(f"\nDownload failed for {filename} (attempt {attempt}/{MAX_RETRIES}): HTTP {response.status_code}")
            except requests.RequestException:
                print(f"\nDownload failed for {filename} (attempt {attempt}/{MAX_RETRIES}).")
        else:
            raise AppError(f"Failed to download {filename} after {MAX_RETRIES} attempts.")
