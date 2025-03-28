import requests
import json
from city_lat_lon import get_lat_lon  

def restaurantId(city_name, restaurant_name):
    # city_name = "Indore"
    # restaurant_name = "Gurukripa Restaurant - Sarwate"

    latitude, longitude = get_lat_lon(city_name)

    url = f"https://www.swiggy.com/dapi/restaurants/search/suggest?lat={latitude}&lng={longitude}&str={restaurant_name.replace(' ', '%20')}&trackingId=undefined&includeIMItem=true"

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        restaurantIdDetails = data.get('data', {}).get('suggestions', [])

        if restaurantIdDetails:
            first_restaurant = restaurantIdDetails[0]  
            metadata_str = first_restaurant.get('metadata')

            if metadata_str:
                try:
                    metadata = json.loads(metadata_str)
                    primaryRestaurantId = metadata.get("data", {}).get("primaryRestaurantId")

                    if primaryRestaurantId:
                        print(f"Primary Restaurant ID: {primaryRestaurantId}")
                        return latitude, longitude, primaryRestaurantId  

                except json.JSONDecodeError:
                    print("Error: Could not decode metadata JSON.")
            else:
                print("No metadata found for the first restaurant.")
        else:
            print("No restaurant suggestions found.")

    print(f"Error: HTTP {response.status_code} - {response.text}")
    return None, None, None  
