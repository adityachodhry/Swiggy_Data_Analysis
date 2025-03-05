import requests
import json
import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",  
    "password": "12345",  
    "database": "restaurant_db",
}

url = "https://www.swiggy.com/dapi/menu/pl?page-type=REGULAR_MENU&complete-menu=true&lat=22.7195687&lng=75.8577258&restaurantId=84070&catalog_qa=undefined&submitAction=ENTER"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.swiggy.com/",
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()  
    print("Data fetched successfully!")

    extracted_items = []

    try:
        # Navigate to the correct path
        menu_sections = (
            data.get("data", {})
            .get("cards", [])[4]  
            .get("groupedCard", {})
            .get("cardGroupMap", {})
            .get("REGULAR", {})
            .get("cards", [])
        )

        for section in menu_sections:
            item_cards = section.get("card", {}).get("card", {}).get("itemCards", [])

            for item in item_cards:
                dish_info = item.get("card", {}).get("info", {})

                if "name" in dish_info and "price" in dish_info:
                    item_data = {
                        "name": dish_info.get("name"),
                        "price": dish_info.get("price") / 100,
                        "rating": dish_info.get("ratings", {}).get("aggregatedRating", {}).get("rating"),
                        "rating_count": dish_info.get("ratings", {}).get("aggregatedRating", {}).get("ratingCountV2"),
                    }
                    extracted_items.append(item_data)

    except Exception as e:
        print(f"Error extracting data: {e}")

    with open("extracted_swiggy_menu.json", "w", encoding="utf-8") as outfile:
        json.dump(extracted_items, outfile, indent=4, ensure_ascii=False)

    print("Extracted data saved to extracted_swiggy_menu.json")
    

    # Insert Data into MySQL Database
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # SQL Query to Insert Data
        insert_query = """
        INSERT INTO menu_items (name, price, rating, rating_count)
        VALUES (%s, %s, %s, %s)
        """

        # Insert each item into the database
        for item in extracted_items:
            cursor.execute(insert_query, (
                item["name"],
                item["price"],
                item["rating"] if item["rating"] is not None else None,
                item["rating_count"] if item["rating_count"] is not None else None
            ))

        connection.commit()  # Commit the transaction
        print("Data inserted into MySQL database successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        connection.close()

else:
    print(f"Failed to fetch data. Status Code: {response.status_code}")
