import requests
import json
import mysql.connector

# Function to fetch and store restaurant data
def fetch_and_store_restaurants():
    url = "https://www.swiggy.com/dapi/restaurants/list/v5?lat=22.7195687&lng=75.8577258&is-seo-homepage-enabled=true&page_type=DESKTOP_WEB_LISTING"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        with open("raw.json", "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

        try:
            restaurants = (
                data.get("data", {})
                .get("cards", [])[1]  
                .get("card", {})
                .get("card", {})
                .get("gridElements", {})
                .get("infoWithStyle", {})
                .get("restaurants", [])
            )

            restaurant_data = []

            for restaurant in restaurants:
                info = restaurant.get("info", {})
                restaurant_id = info.get("id")
                restaurant_name = info.get("name")

                if restaurant_id and restaurant_name:  
                    restaurant_data.append((restaurant_id, restaurant_name))  

            # Store data in MySQL database
            store_in_database(restaurant_data)

        except Exception as e:
            print(f"Error extracting restaurant data: {e}")

    else:
        print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")


# Function to store data in MySQL
def store_in_database(data):
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",      # Replace with your MySQL username
            password="12345",  # Replace with your MySQL password
            database="restaurant_db"
        )
        cursor = connection.cursor()

        # Insert restaurant data
        query = "INSERT INTO restaurants_list (id, name) VALUES (%s, %s) ON DUPLICATE KEY UPDATE name = VALUES(name)"
        cursor.executemany(query, data)

        # Commit and close connection
        connection.commit()
        print(f"{cursor.rowcount} records inserted successfully.")
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")


# Run the function
fetch_and_store_restaurants()
