import urllib.request
import json
import ssl
 #url = f"
 #http:
 #//api.zippopotam.us/us/{user_zip}
#context = ssl._create_unverified_context()
API_KEY = "Jo48Jpu4ymO8Sgq5ZIlKP7EASBDm9lEt6sGctOCo4u4iu1Dduot4cdStdX4TyXp3"
def get_zip_radius(user_zip,radius):
    url = f"https://www.zipcodeapi.com/rest/{API_KEY}/radius.json/{user_zip}/{radius}/miles"
    context = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(url, context = context) as response:
            data = json.loads(response.read().decode())
            #result = 
            if 'user_zips' in data:
                return  [z['user_zip'] for z in data['user_zips']]
            else:
                print("\nAPI response missing expected 'zip_codes' field.")
                print("Raw response:", data)
                return []
    except urllib.error.HTTPError as e:
        print(f"\nHTTP Error {e.code}: {e.reason}")
        try:
            error= e.read().decode()
        except:
            print("no error message")
        return []
    except urllib.error.URLError as e:
        print(f"\nURL Error",{e.reason})
        return []

    
user_zip = input("Enter your zip code: ")
#user_zip_data = zip_to_coords(user_zip)
zip_radius = get_zip_radius(user_zip, 20)

#if user_zip_data:
 #   place = user_zip_data['places'][0]
  #  print(f"\nZIP Code Info for {user_zip}:")
   # print(f"City: {place['place name']}")
#    print(f"State: {place['state']}")
 #   print(f"Latitude: {place['latitude']}")
  #  print(f"Longitude: {place['longitude']}")
#else:
 #   print("No data found. Please check the ZIP code and try again.")
print(f"ZIP Codes within 20 miles of {user_zip}:")
print(zip_radius)