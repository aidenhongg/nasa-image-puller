"""NASA Image Puller - Downloads APOD images matching a search query."""

import sys

from modules.globals import AppError
from modules.input_handler import get_inputs, search_descriptions
from modules.connection_handler import build_url, get_result, download_images


def main():
    """Run the NASA Image Puller: prompt for inputs, search, and download."""
    try:
        start_date, end_date, query = get_inputs()
        url = build_url(start_date, end_date)
        results = get_result(url)
        image_urls = search_descriptions(results, query)
        download_images(image_urls)
    except AppError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
