# nasa-image-puller
Downloads two relevant pictures from the APOD NASA database based on a date range and query.
Run main.py to launch.

The program takes a date range and a single query.
The two images in APOD within that range that have the most and second-most query hits will be downloaded to ./image1.jpg and ./image2.jpg, respectively.

A valid APOD API key should be put into NASA_API_KEY.txt. You can get this at: https://api.nasa.gov/#signUp
A valid date range must be given, which must be within June 16, 1995 to the present day. If the date range is unbounded, it will default to January 1, 2024.

This was one of my first projects ever. The program functions fine, albeit a little slow, so the search function could be optimized. 
This was when I didn't know much about time complexity, so there are some unnecessary type conversions that each add n iterations.

The tests were written for a different SimpleImage library, so they do not validate properly. This will have to be fixed later.
