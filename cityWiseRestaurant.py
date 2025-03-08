import requests
import json
from city_lat_lon import get_lat_lon  


cityName = "Indore"
restaurantName = "Gurukripa Restaurant - Sarwate"

latitude, longitude = get_lat_lon(cityName)

url = f"https://www.swiggy.com/dapi/restaurants/search/suggest?lat={latitude}&lng={longitude}&str={restaurantName.replace(' ', '%20')}&trackingId=undefined&includeIMItem=true"

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json() 

    with open('cityRaw.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    print("Data saved to cityRaw.json successfully!")

    restaurantIdDetails = data.get('data', {}).get('suggestions', [])

    if restaurantIdDetails:
        first_restaurant = restaurantIdDetails[0]  
        metadata_str = first_restaurant.get('metadata')

        if metadata_str:
            try:
                metadata = json.loads(metadata_str)
                primaryRestaurantId = metadata.get("data", {}).get("primaryRestaurantId")

                if primaryRestaurantId:
                    print(f"Primary Restaurant ID (First Entry): {primaryRestaurantId}")
                else:
                    print("Primary Restaurant ID not found in metadata.")

            except json.JSONDecodeError:
                print("Error: Could not decode metadata JSON.")
        else:
            print("No metadata found for the first restaurant.")
    else:
        print("No restaurant suggestions found.")

else:
    print(f"Error: HTTP {response.status_code} - {response.text}")

