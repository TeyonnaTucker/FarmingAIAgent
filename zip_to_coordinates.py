
import urllib.request
import json

def get_zip_info(user_zip):
    url = f"https://api.zippopotam.us/us/{user_zip}"
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            result = json.loads(data)
            return result
    except urllib.error.HTTPError as e:
        print(f"Error: Unable to fetch data for ZIP code {user_zip}.")
        return None

# Get ZIP code from user
user_zip = input("Enter your ZIP code: ")

# Fetch and display location info
user_zip_data = get_zip_info(user_zip)

if user_zip_data:
    area = user_zip_data['places'][0]
    print(f"\nZIP Code Info for {user_zip}:")
    print(f"City: {area['place name']}")
    print(f"State: {area['state']}")
    print(f"Latitude: {area['latitude']}")
    print(f"Longitude: {area['longitude']}")
else:
    print("No data found. Please check the ZIP code and try again.")