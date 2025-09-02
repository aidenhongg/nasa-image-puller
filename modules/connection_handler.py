import requests

from modules.globals import *

# Helper function to build the URL for querying the API
def build_url(start_date: str, end_date: str) -> str:

    # Default to January 2024 if there is none for either start or end date
    if not start_date:
        start_date = '2024-01-01'
    if not end_date:
        end_date = '2024-01-31'

    # Compiled URL - URL, API, then dates
    return (BASE_NASA_URL + NASA_API_KEY +
            "&start_date=" + start_date + "&end_date=" + end_date)


# Function to get results from the NASA APOD API
def get_result(url: str) -> dict:
    # If connection fails program only tries three times
    for failures in range(3):
        try:
            # Open connection
            response = requests.get(url)

            # Only get and return response if response code is valid
            if response.status_code == 200:
                return response.json()

            # If in any case connection fails - add 1 to counter and continue loop
            else:
                # Alert user how many times it failed
                print("\nConnection failed " +
                      str(failures + 1) + " times. Trying again...")
                continue

        # If in any case connection fails - add 1 to counter and continue loop
        except Exception:
            print("\nConnection failed " +
                  str(failures + 1) + " times. Trying again...")
            continue

    # If function has reached this point without returning -> connection failed -> raise error
    raise AppError

# Function to download images based on the filtered results
def get_images(urls : iter) -> None:

    # We cannot run without two images - raise Error
    if not urls[0] or not urls[1]:
        raise ValueError("Not enough URLs!")

    # img tracks which image we're saving
    img = 1
    for url in urls:

        # Failure switch for if we fail more than 3 times on either image - True on each iteration
        is_failure = True
        for failures in range(3):
            try:

                # Connect
                response = requests.get(url)

                # Only get image if response code is valid
                if response.status_code == 200:

                    with open("image" + str(img) + ".jpg", 'wb') as file:
                        file.write(response.content)

                    # Only then do we continue loop and set Failure switch to false
                    img += 1
                    is_failure = False
                    break

                # In any case that we fail continue failure loop and update counter
                else:
                    print("\nConnection failed " +
                          str(failures + 1) + " times. Trying again...")
                    continue

            # In any case that we fail continue failure loop and update counter
            except Exception as e:
                print("\nConnection failed " +
                      str(failures + 1) + " times. Trying again...")
                continue
        # Loop only reaches this point if we failed more than 3 times for either image - raise error and exit
        if is_failure:
            raise AppError
