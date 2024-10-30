import requests
import json
import pandas as pd
import time
from datetime import datetime as dt
from searchWebsite import find_official_website
from generateCSV import generateCSV


with open('categories_listing.json', 'r') as file:
    category_data = json.load(file)

def convert_business_hours(business_hours):
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    #output format {'Mon': '10:00 AM - 10:00 PM'}
    business_hours_dict = {day: 'Closed' for day in days_of_week}

    #populate business hours while converting 24hr to 12hr format
    for business_hour in business_hours:
        day_index = days_of_week[business_hour['day']] #weekday
        start_time = business_hour['start'] #opening hour
        end_time = business_hour['end'] #closing hour

        # #formating to HR:MM 24 hr
        start_time_24hr = dt.strptime(f"{start_time[:2]}:{start_time[2:]}", "%H:%M")
        end_time_24hr = dt.strptime(f"{end_time[:2]}:{end_time[2:]}", "%H:%M")

        
        #format to HR:MM 12hr
        start_time_12hr = dt.strftime(start_time_24hr,"%I:%M %p")
        end_time_12hr = dt.strftime(end_time_24hr,"%I:%M %p")

        business_hours_dict[day_index] = f"{start_time_12hr} - {end_time_12hr}"
    
    return business_hours_dict

category_titles = []

def scrape_website(search_info):
    category_titles.extend(search_info["categories"])
    aliases = [category["alias"] for category in category_data if category["title"].lower() in category_titles]

    #changing given input categories to its aliases
    search_info['categories'] = aliases

    business_data = get_business_data(search_info)
    return business_data

def get_business_data(search_info):
    url = f'https://api.yelp.com/v3/businesses/search'
    headers = {
        'Authorization': f'Bearer {search_info["api_key"]}'
        }
    params = {
        'term': search_info["term"],
        'location': search_info["location"],
        'categories': search_info["categories"],
        'limit': 50
    }
    offset = 0
    # table_data = []
    total_businesses_data = []

    # Keep track of total number of businesses collected
    total_collected = 0

    while True:
        params['offset'] = offset
        response = requests.get(url, headers=headers, params=params)
        
        # Error handling for failed requests
        if response.status_code != 200:
            return f'Error: Received status code {response.status_code}'

        data = response.json()
        if data:
            businesses = data["businesses"]
            business_count = len(businesses)

            for business in businesses:
                categories_list = [category['title'] for category in business["categories"]]
                hours = convert_business_hours(business['business_hours'][0]['open']) if len(business['business_hours']) else 'There are no business hours.'
                    
                website_url = find_official_website(business["alias"]) 

                business_info = {
                    "id": business["id"],
                    "business_title": business["name"],
                    "alias": business["alias"],
                    "categories": categories_list,
                    "address": business["location"]["address1"],
                    "city": business["location"]["city"],
                    "state": business["location"]["state"],
                    "country": business["location"]["country"],
                    "zip_code": business["location"]["zip_code"],
                    "display_address": business["location"]["display_address"],
                    "phone": business["phone"],
                    "display_phone": business['display_phone'],
                    "business_hours": hours,
                    "business_website": website_url
                } 
                total_businesses_data.extend([business_info])

            # business_ids.extend([business['id'] for business in businesses])
            total_collected += business_count

            if business_count < 50:
                return "No more businesses to retrieve."
                break

            # for business_id in business_ids:
            offset += 50  # Move to the next page
            if offset ==200:
                params["limit"] = 40

            # API limit of 1000 businesses
            if offset >= 1000:
                return "Reached API limit of 1000 businesses."
                break

        else:
            return "Error: No businesses found or an error occurred."
            break   
    try:
        file_title_to_save = f"{params['term']}-{'-'.join([location_string.strip() for location_string in params['location'].split(',')])}{'-'if len(category_titles) else ''}{'-'.join(category_titles) if len(category_titles)>1 else category_titles[0]}.csv"
        result = generateCSV(total_businesses_data, file_title_to_save)
        return result

    except Exception as e:
        return f'Error: CSV file generation failed. {e}'