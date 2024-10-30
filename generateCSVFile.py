import streamlit as st
import os
import csv
import pandas as pd


# business_info = [
#     {
#         "business_title": "title1",
#         "city": "city1",
#         "state": "CA",
#         "zip_code": "12345",
#         "display_phone": "123-456-7890",
#         "business_website": "https://business3.com",
#         "categories": ["Category1", "Category2"]
#     },
#     {
#         "business_title": "title2",
#         "city": "city2",
#         "state": "NY",
#         "zip_code": "54321",
#         "display_phone": "098-765-4321",
#         "business_website": "https://business5.com",
#         "categories": ["Category3", "Category4"]
#     },
#     {
#         "business_title": "title1",
#         "city": "city1",
#         "state": "CA",
#         "zip_code": "12345",
#         "display_phone": "123-456-7890",
#         "business_website": "https://business5.com",
#         "categories": ["Category1", "Category2"]
#     },
#     {
#         "business_title": "title2",
#         "city": "city4",
#         "state": "CA",
#         "zip_code": "38928",
#         "display_phone": "123-456-7890",
#         "business_website": "https://business4.com",
#         "categories": ["Category1", "Category2",  "Category4", "Category3"]
#     },
#     {
#         "business_title": "title2",
#         "city": "city2",
#         "state": "NY",
#         "zip_code": "54321",
#         "display_phone": "098-765-4321",
#         "business_website": "https://business5.com",
#         "categories": ["Category3", "Category4"]
#     }
# ]

# # Sample state abbreviations
# states_with_abbrevations = {
#     "CA": "California",
#     "NY": "New York"
# }

# # Sample categories list
# categories_list = ["Category1", "Category2", "Category3", "Category4", "Category5"]

# # Create formatted information
# formated_info = []
# for info in business_info:
#     categories_list_filtered = [cat for cat in categories_list if cat in info["categories"]]

#     formated_info.append({
#         "Listing Title": info["business_title"],
#         "Listing SEO Title": f"{info['business_title']} {info['city']}",
#         "Listing Email": "",
#         "Listing URL": info["business_website"],
#         "Listing Address": "address",  # Placeholder for address
#         "Listing Address2": "",
#         "Listing country": 'United States',
#         "Listing Country Abbrevation": "US",
#         "Listing Region": "",
#         "Listing Region Abbrevation": "",
#         "Listing State": states_with_abbrevations.get(info["state"], ""),
#         "Listing State Abbrevation": info["state"],
#         "Listing City": info["city"],
#         "Listing City Abbrevation": "",
#         "Listing Neighborhood": "",
#         "Listing Neighborhood Abbrevation": "",
#         "Listing Postal Code": info["zip_code"],
#         "Listing Latitude": "",
#         "Listing Longitude": "",
#         "Listing Phone": info["display_phone"],
#         "Listing Short Description": "",
#         "Listing Long Description": "",
#         "Listing SEO Description": "",
#         "Listing Keywords": "",
#         "Listing Renewal Data": "",
#         "Listing Status": "Active",
#         "Listing Level": "Silver",
#         "Listing Category 1": categories_list_filtered[0] if len(categories_list_filtered) > 0 else '',
#         "Listing Category 2": categories_list_filtered[1] if len(categories_list_filtered) > 1 else '',
#         "Listing Category 3": categories_list_filtered[2] if len(categories_list_filtered) > 2 else '',
#         "Listing Category 4": categories_list_filtered[3] if len(categories_list_filtered) > 3 else '',
#         "Listing Category 5": categories_list_filtered[4] if len(categories_list_filtered) > 4 else '',
#         "Listing Template": "New Listing Template",
#         "Listing DB id": "",
#         "Custom ID": "",
#         "Account Username": "",
#         "Account Password": "",
#         "Account Contact First Name": "",
#         "Account Contact Last Name": "",
#         "Account Contact Company": "",
#         "Account Contact Address": "",
#         "Account Contact Address2": "",
#         "Account Contact Country": "",
#         "Account Contact State": "",
#         "Account Contact City": "",
#         "Account Contact Postal Code": "",
#         "Account Contact Phone": "",
#         "Account Contact Email": "",
#         "Account Contact URL": "",
#     })

# # Create DataFrame from formatted information
# data = pd.DataFrame(formated_info)

#specify the path of the directory you want to fetch the csv files
directory = '/Users/sarikamangalpally/Documents/i3dev/Listing Files'

#specify the path of the csv file you want to save
def list_csv_files(directory):
    #list all the csv files in the specified path
    return [file for file in os.listdir(directory) if file.endswith('.csv')]

def append_to_csv(data):
    csv_files = list_csv_files(directory)
    try:
        if csv_files:
            # Select the file to append to
            append_to_file_name = st.selectbox('Select the CSV file to append', csv_files, index=None, placeholder='Select the file..')
            append_to_file_path = os.path.join(directory, append_to_file_name)

            # Check if the file is empty or not
            file_is_empty = os.path.getsize(append_to_file_path) == 0

            existing_data = pd.read_csv(append_to_file_path)
            
            # Concatenate and drop duplicates
            combined_data = pd.concat([existing_data, data]).drop_duplicates(keep='first', ignore_index=True)
            
            # Identify only the new rows to append
            new_rows = combined_data.loc[~combined_data.index.isin(existing_data.index)]

            if not new_rows.empty:
                new_rows.to_csv(append_to_file_path, mode='a', index=False, header=file_is_empty)
                return f'{len(new_rows)} new row(s) successfully appended to {append_to_file_name}'
            else:
                st.info("No new data to append. All rows are duplicates.")
                return "No new data to append. All rows are duplicates."
            # Append the data to the file, Include header if the file is empty
            # data.to_csv(append_to_file_path, mode='a', index=False, header=file_is_empty)  
            return f'Data is successfully appended to {append_to_file_name}'
        else:
            return 'No CSV files found in the current directory. Please create new CSV file.'

    except Exception as e:
        st.error(f'Error in appending the data to {append_to_file_name}.csv file: {e}')
        return f'Error in appending the data to {append_to_file_name}.csv file: {e}'
        st.write(csv_files)

def create_new_file(data):
    print('entered create new file function')
    try:
        new_file_name = st.text_input('Enter the name for the new CSV file (with .csv extension):')
        if new_file_name:
            data.to_csv(new_file_name, index=False)
            return f'Success: {new_file_name} file generated.'
        else:
            return 'Please enter a file name.'
    except Exception as e:
        return f'{e}'

def generateCSV(data):    
    st.title('CSV File Generation')
    options = ['Create a new CSV file', 'Append to existing CSV file']
    option = st.selectbox('What would you like to do?', options, index=0)
    selected_option = options.index(option)
    try:
        result = create_new_file(data) if selected_option == 0 else append_to_csv(data)
        return result
    except Exception as e:
        return f'Error: Select correct option to perform operation  {e}'


# print(generateCSV(data))