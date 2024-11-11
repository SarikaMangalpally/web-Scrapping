import streamlit as st
import os
import pandas as pd

def ensure_directory_exists(full_directory):
    #Create the directory if it doesn't already exist.
    if not os.path.exists(full_directory):
        os.makedirs(full_directory)
        st.info(f"Directory created.")

def update_selected_option():
    st.session_state.selected_option = st.session_state['action_for_csv_file_generation']
    # Reset the append button session when changing options
    st.session_state.append_file_button_session = False

def set_append_file_button_session():
    st.session_state.append_file_button_session = True

    
#specify the path of the csv file you want to save
def list_csv_files(full_directory):
    #list all the csv files in the specified path
    return [file for file in os.listdir(full_directory) if file.endswith('.csv')]

def identify_duplicates(existing_data, new_data):
    duplicates = existing_data.merge(new_data, on=["Listing Title", "Listing Address"], suffixes=('_old', '_new'))

    duplicate_records = []

    for _, row in duplicates.iterrows():
        old_row = row.filter(regex='_old').to_dict()
        new_row = row.filter(regex='_new').to_dict()
        
        # Append each old/new pair as a record with keys for clear identification
        duplicate_records.append({'Old': old_row, 'New': new_row})

    # Convert the list of duplicate records into a DataFrame
    duplicate_df = pd.DataFrame(duplicate_records)
    
    st.write("Duplicate Records:")
    st.write(duplicate_df)

    return duplicate_df

def append_to_csv(data, full_directory):
    ensure_directory_exists(full_directory)
    csv_files = list_csv_files(full_directory)
    try:
        if csv_files:
            # Select the file to append to
            append_to_file_name = st.selectbox('Select the CSV file to append', csv_files, index=None, placeholder='Select the file..', key='append_to_file_select')
            if st.button('Append file', on_click=set_append_file_button_session) or st.session_state.append_file_button_session:
                # Append data to the selected file
                append_to_file_path = os.path.join(full_directory, append_to_file_name)

                # Check if the file is empty or not
                file_is_empty = os.path.getsize(append_to_file_path) > 0
                
                st.write(f'new data length: {len(data)}')

                # Load existing data from the file
                if file_is_empty:
                    existing_data = pd.read_csv(append_to_file_path)
                else:
                    existing_data = pd.DataFrame(columns=data.columns)  # Empty DataFrame with the same columns as `data`
                    st.write(f'existing data length: {len(existing_data)}')
                
                duplicates = identify_duplicates(existing_data, data)

                # Remove duplicates from existing_data based on 'Listing Title' and 'Listing Address'
                existing_data = existing_data[~existing_data.set_index(["Listing Title", "Listing Address"]).index.isin(
                    data.set_index(["Listing Title", "Listing Address"]).index
                )]

                # Concatenate existing data with new data and remove duplicates, keeping only the latest
                updated_data = pd.concat([existing_data, data]).drop_duplicates(subset=["Listing Title", "Listing Address"], keep='last')

                if not updated_data.empty:
                    # Save the updated data back to the CSV file
                    updated_data.to_csv(append_to_file_path, mode='w', index=False, header=True)
                    
                    del st.session_state.append_file_button_session

                    return f'{len(updated_data)} new row(s) successfully appended to {append_to_file_name}'
                else:
                    st.info("No new data to append. All rows are duplicates.")
                    return "No new data to append. All rows are duplicates."

            else:
                st.warning("Append file button is not clicked")
        else:
            st.warning('No CSV files found in the current directory. Please create new CSV file.')

    except Exception as e:
        st.error(f'Error in appending the data to {append_to_file_name}.csv file: {e}')
        return f'Error in appending the data to {append_to_file_name}.csv file: {e}'

def create_new_file(data, full_directory):
    ensure_directory_exists(full_directory)
    new_file_name = st.text_input('Enter the name for the new CSV file (with .csv extension):', key='new_file_name_input')
    try:
        if st.button('Create new file') and new_file_name.endswith('.csv'):
            new_file_path = os.path.join(full_directory, new_file_name)
            data.to_csv(new_file_path, index=False)
            return f'Success: {new_file_name} file generated.'
        else:
            st.warning('Please enter a file name.')
    except Exception as e:
        return f'{e}'


def generate_csv(data, location):
    directory = '/Users/sarikamangalpally/Documents/i3dev/Listing Files/'
    location = '-'.join(location.split(', ')).lower()
    options = ['Create a new CSV file', 'Append to existing CSV file']

    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = options[0]
    
    if 'append_file_button_session' not in st.session_state:
        st.session_state.append_file_button_session = False

    st.selectbox(
        'What would you like to do?',
        options, 
        index=options.index(st.session_state.selected_option),
        on_change=update_selected_option, 
        key='action_for_csv_file_generation'
    )

    selected_option_index = options.index(st.session_state.selected_option)
    try:
        full_directory = os.path.join(directory, location)
        result = create_new_file(data, full_directory) if selected_option_index == 0 else append_to_csv(data, full_directory)
        return result
    except Exception as e:
        st.warning(f'Error: Select correct option to perform operation  {e}')