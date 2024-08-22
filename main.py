import requests
import json
from datetime import datetime
from feedgen.feed import FeedGenerator
import time

# Function to generate the current date in the required format (YYYY-MM-DD)
def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

# Generate URLs dynamically based on the current date
def generate_dining_court_urls(date):
    base_url = "https://api.hfs.purdue.edu/menus/v2/locations/"
    dining_courts = ["Windsor", "Wiley", "Ford", "Hillenbrand", "Earhart"]
    return {court: f"{base_url}{court}/{date}" for court in dining_courts}

# Function to fetch menu data with error handling and retries
def fetch_menu_data(url, retries=3):
    for _ in range(retries):
        response = requests.get(url)
        if response.status_code == 200:
            try:
                return response.json()  # Parse the response as JSON
            except json.JSONDecodeError:
                print(f"Failed to parse JSON response from {url}")
                return None
        else:
            print(f"Failed to fetch data from {url} with status code {response.status_code}. Retrying...")
            time.sleep(2)  # Wait for 2 seconds before retrying
    return None

# Function to parse the JSON menu data
def parse_menu_data(json_data):
    items = []
    if json_data is None:
        return items

    current_time = datetime.now().strftime("%H:%M:%S")

    for meal in json_data.get('Meals', []):
        meal_name = meal['Name']
        hours = meal.get('Hours')
        
        # Ensure hours exist, if not, skip this meal
        if hours:
            start_time = hours.get('StartTime', '00:00:00')
            end_time = hours.get('EndTime', '23:59:59')

            # Include only meals currently being served
            if start_time <= current_time <= end_time:
                # Convert times to AM/PM format
                start_time_am_pm = datetime.strptime(start_time, "%H:%M:%S").strftime("%I:%M %p")
                end_time_am_pm = datetime.strptime(end_time, "%H:%M:%S").strftime("%I:%M %p")
                meal_time = f"{start_time_am_pm} - {end_time_am_pm}"

                for station in meal.get('Stations', []):
                    station_name = station['Name']
                    for item in station.get('Items', []):
                        item_name = item['Name']
                        items.append((meal_name, meal_time, station_name, item_name))
    
    return items

# Function to create the RSS feed
def create_rss_feed(dining_court_menus):
    fg = FeedGenerator()
    fg.title("Purdue Dining Court Menu")
    fg.link(href="http://www.purdue.edu/dining/menus", rel="alternate")
    fg.description("Current meals being served at Purdue dining courts")
    fg.language("en")

    for court_name, menu_items in dining_court_menus.items():
        # Group items by meal and time
        meals = {}
        for meal_name, meal_time, station_name, item_name in menu_items:
            key = (meal_name, meal_time)
            if key not in meals:
                meals[key] = {}
            if station_name not in meals[key]:
                meals[key][station_name] = []
            meals[key][station_name].append(item_name)

        # Create RSS entries
        for (meal_name, meal_time), stations in meals.items():
            fe = fg.add_entry()
            fe.title(f"{court_name} - {meal_name} - {meal_time}")
            fe.link(href="http://www.purdue.edu/dining/menus")

            # Construct the description with HTML, including additional line breaks for readability
            description = ""
            for station_name, items in stations.items():
                description += f"<p>{station_name}: {', '.join(items)}.</p><br>"

            fe.description(description.strip())  # Remove trailing whitespace

    fg.rss_file("purdue_menu_rss.xml")

# Main function to coordinate the script
def main():
    current_date = get_current_date()
    dining_court_urls = generate_dining_court_urls(current_date)
    
    dining_court_menus = {}
    for court, url in dining_court_urls.items():
        json_data = fetch_menu_data(url)
        dining_court_menus[court] = parse_menu_data(json_data)

    create_rss_feed(dining_court_menus)

if __name__ == "__main__":
    main()
