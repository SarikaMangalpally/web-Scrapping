import json
import format_categories
import pandas as pd

with open('state_abbrevations.json', 'r') as file:
    data = json.load(file)
    states_with_abbrevations = data['states']['abbrevations']

with open('categories_listing.json', 'r') as file:
    data = json.load(file)
    categories = data

def generateCSV(business_info, title_to_save):
    # Create a dictionary to store the data
    data = []
    for info in business_info:
        *categories_list, = format_categories.get_category_paths(info["categories"])

        formated_info = {
            "Listing Title": info["business_title"],
            "Listing SEO Title": info["business_title"] + info["city"],
            "Listing Email": "",
            "Listing URL": info["business_website"],
            "Listing Address": info["address"],
            "Listing Address2": "",
            "Listing country": 'United States',
            "Listing Country Abbrevation": info["country"],
            "Listing Region": "",
            "Listing Region Abbrevation": "",
            "Listing State": states_with_abbrevations[info["state"]],
            "Listing State Abbrevation": info["state"],
            "Listing City": info["city"],
            "Listing City Abbrevation": "",
            "Listing Neighborhood": "",
            "Listing Neighborhood Abbrevation": "",
            "Listing Postal Code": info["zip_code"],
            "Listing Latitude": "",
            "Listing Longitude": "",
            "Listing Phone": info["display_phone"],
            "Listing Short Description": "",
            "Listing Long Description": "",
            "Listing SEO Description": "",
            "Listing Keywords": "",
            "Listing Renewal Data": "",
            "Listing Status": "Active",
            "Listing Level": "Silver",
            "Listing Category 1":  categories_list[0] if len(categories_list)>0 else'',
            "Listing Category 2": categories_list[1] if len(categories_list)>1 else'',
            "Listing Category 3": categories_list[2] if len(categories_list)>2 else'',
            "Listing Category 4": categories_list[3] if len(categories_list)>3 else'',
            "Listing Category 5": categories_list[4] if len(categories_list)>4 else'',
            "Listing Template": "New Listing Template",
            "Listing DB id": "",
            "Custom ID": "",
            "Account Username": "",
            "Account Password": "",
            "Account Contact First Name": "",
            "Account Contact Last Name": "",
            "Account Contact Company": "",
            "Account Contact Address": "",
            "Account Contact Address2": "",
            "Account Contact Country": "",
            "Account Contact State": "",
            "Account Contact City": "",
            "Account Contact Postal Code": "",
            "Account Contact Phone": "",
            "Account Contact Email": "",
            "Account Contact URL": "",
        }
        data.extend([formated_info])
    if data:
        try:
            df = pd.DataFrame(data)
            df.to_csv(title_to_save, index=False)
            return 'Success: CSV file generated.'
        except Exception as e:
            return f'Error: CSV file generation failed. {e}'
    else:
        return 'Error: No data to save in CSV file.'