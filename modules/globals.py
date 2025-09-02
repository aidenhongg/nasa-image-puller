# NASA API Key
with open('./NASA_API_KEY.txt', 'r') as file:
    NASA_API_KEY = file.readline()

BASE_NASA_URL = 'https://api.nasa.gov/planetary/apod?api_key='

# When fatal error occurs AppError is called
class AppError(Exception):
    def __init__(self):
        self.error = Exception
