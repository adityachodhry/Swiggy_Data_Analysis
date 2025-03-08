import requests
import time

def get_lat_lon(city_name):
    url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json"

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        
        if response.status_code != 200:
            print(f"Error: HTTP {response.status_code}")
            print("Response:", response.text)  
            return None

        data = response.json()
        
        if data:
            lat = data[0]["lat"]
            lon = data[0]["lon"]
            return lat, lon
        else:
            print("No results found for", city_name)
            return None

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None
    except ValueError:
        print("Invalid JSON response")
        return None

# city = "Mumbai"
# latitude, longitude = get_lat_lon(city)

# if latitude and longitude:
#     print(f"Latitude: {latitude}, Longitude: {longitude}")
# else:
#     print("Failed to retrieve location.")
