import sys

from modules import *

# Main function to run the complete process
def run():
    # Try loop if any fatal errors happen
    try:
        # Save start, end, and query to tuple
        start_date, end_date, query = input_interfacer.get_inputs()

        # Build URL using tuple
        url = connection_handler.build_url(start_date, end_date)

        # Get all image results and save to dictionary
        image_dict = connection_handler.get_result(url)

        # Get desired image URLs
        image_urls = input_interfacer.search_description(image_dict, query)

        # Save to image1.jpg and image2.jpg based on URLs
        connection_handler.get_images(image_urls)

    # If fatal error happens
    except AppError as e:
        # Alert user of error and exit program
        print(e)
        sys.exit(1)


# Main function to run
if __name__ == '__main__':
    run()
