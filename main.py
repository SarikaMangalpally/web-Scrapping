import streamlit as st
from scrape import scrape_website
from generate_csv_file import generate_csv
import pandas as pd
import re


def scrape_site():
    st.title('Web Scrapper')

    term = st.text_input("Enter Category to search. Example: 'Restaurant/Coffee' ")
    location = st.text_input("Enter Location for search. Example: 'NewYork, NY' ")
    categories = st.text_input("Enter the Category or multiple categories you want to search. Example: 'gym, french'. ")

    pattern = r"'([^']*)'|([^,]+)"
    matches = re.findall(pattern, categories)

    # Extract the matched categories
    categories_list = [match[0] if match[0] else match[1] for match in matches]
    
   # Strip whitespace and convert to lowercase
    categories_list = [category.strip().lower() for category in categories_list]
    # st.write(categories_list)
    api_key = 'DJpPHlmlFma1V1x7PV3ZXkpUVxh5oyA4ipNIelEqyTwRTz0sxMRqRbyIV3uXR7rL-0mvt3C7OAYHMum6mx0OOzvOrBFM_BUbJqcsn9o5ITPXfv1oWpIJdBGpt2k-Z3Yx'
    # api_key = '490Tu7FaGelk7XVYBBOXwejO2cioxGmPjG0gT-R6E-DfTe5qAxzAuoXGRqTkn5fQYZoCbXbKgIUbqtW_SEVaNLTJbbcWvazO8wfRKMznhWVZ_ydAdb0xiAq89M8fZ3Yx'
    search_info = {
        'term': term,
        'location': location,
        'categories': categories_list,
        'api_key': api_key
    } 
    if st.button('Scrape Site'):
        if search_info != st.session_state.get("last_search_info"):
            # New search, update session state
            st.session_state.last_search_info = search_info
            st.write('Scraping the website...')
            result = scrape_website(search_info)

            # Check and store results if available
            if isinstance(result, pd.DataFrame) and not result.empty:
                st.session_state.business_data = result
                st.session_state.current_action = 'Generate CSV'
                st.rerun()
            else:
                st.write("No results found.")
        else:
                st.write("You have already scraped for this search. Please change the input for a new search.")



def generate_csv_action():
    st.header("CSV File Generation")
    if 'business_data' in st.session_state and not st.session_state.business_data.empty:
        st.write('Generating CSV file...')
        result = generate_csv(st.session_state.business_data, st.session_state.last_search_info["location"])

        if result:
            st.write(result)

        # Display Continue and Exit buttons after generating CSV
        if st.button("Continue"):
            st.session_state.current_action = 'Scrape Site'  # Set to Scrape Site for continuing
            st.rerun()  # Rerun to return to "Scrape Site" view

        if st.button("Exit"):
            st.session_state.current_action = 'Exit'  # Set to Exit
            st.rerun()



def main():
    if 'current_action' not in st.session_state:
        st.session_state.current_action = 'Scrape Site'
    
    if st.session_state.current_action == 'Exit':
        st.write("Exiting the application...")
        st.stop()
    
    if st.session_state.current_action == 'Scrape Site':
        # st.title('Web Scrapper')
        scrape_site()
    elif st.session_state.current_action == 'Generate CSV':
        generate_csv_action()

        

            

        # if 'scrape_button_session' not in st.session_state:
        #     st.session_state.scrape_button_session = False
        
        # def set_button_session():
        #     st.session_state.scrape_button_session = True

        # if (st.button('Scrape Site', on_click=set_button_session) or st.session_state.scrape_button_session):
        #     if search_info not in st.session_state:
        #         st.session_state.search_info = search_info
            
        #     st.write('Scraping the website...')
        #     result = scrape_website(search_info)

        #     if isinstance(result, pd.DataFrame) and not result.empty:
        #         st.session_state.business_data = result
        #         st.session_state.current_action = 'Generate CSV'

        #         st.rerun()  
        #     else:
        #         st.write("No results found")

    # elif st.session_state.current_action == 'Generate CSV':
    #     st.header("CSV File Generation")
    #     if 'business_data' in st.session_state and not st.session_state.business_data.empty:
    #         st.session_state.current_action = 'Generate CSV'
    #         st.write('Generating CSV file...')
    #         result = generate_csv(st.session_state.business_data, st.session_state.search_info["location"])

    #         if result:
    #             st.write(result)

    #         # Display Continue and Exit buttons after generating CSV
    #         if st.button("Continue"):
    #             st.session_state.current_action = 'Scrape Site'  # Set to Scrape Site for continuing
    #             st.rerun()  # Rerun to return to "Scrape Site" view

    #         if st.button("Exit"):
    #             st.session_state.current_action = 'Exit'  # Set to Exit
    #             st.rerun()  # Rerun to process the exit condition



if __name__=="__main__":
    main()