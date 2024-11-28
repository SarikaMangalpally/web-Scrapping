import requests
import json

api_key = 'DJpPHlmlFma1V1x7PV3ZXkpUVxh5oyA4ipNIelEqyTwRTz0sxMRqRbyIV3uXR7rL-0mvt3C7OAYHMum6mx0OOzvOrBFM_BUbJqcsn9o5ITPXfv1oWpIJdBGpt2k-Z3Yx'
# api_key = '490Tu7FaGelk7XVYBBOXwejO2cioxGmPjG0gT-R6E-DfTe5qAxzAuoXGRqTkn5fQYZoCbXbKgIUbqtW_SEVaNLTJbbcWvazO8wfRKMznhWVZ_ydAdb0xiAq89M8fZ3Yx'
def get_categories_with_alias():

    url = "https://api.yelp.com/v3/categories"
    headers = {
        "Authorization": f'Bearer {api_key}'
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    updated_data = []
    for item in data["categories"]:
        filtered_item = {
        "title": item["title"],
        "alias": item["alias"],
        "parent_aliases": item["parent_aliases"][0] if item["parent_aliases"] else ''
        }
        updated_data.append(filtered_item)
    try:
        with open('categories_listing.json', 'w') as file:
            json.dump(updated_data, file, indent=4)
        return 'Successfull'
    except Exception as e:
        return f'Failed to add data: {e}'

get_categories_with_alias()