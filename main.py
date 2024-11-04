import streamlit as st
from scrape import (get_business_data, scrape_website)

st.title('AI web scrapper')

term = st.text_input("Enter Category to search. Example: 'Restaurant/Coffee' ")
location = st.text_input("Enter Location for search. Example: 'NewYork, NY' ")
categories = st.text_input("Enter the Category or multiple categories you want to search. Example: 'gym, french'. ")
api_key = '490Tu7FaGelk7XVYBBOXwejO2cioxGmPjG0gT-R6E-DfTe5qAxzAuoXGRqTkn5fQYZoCbXbKgIUbqtW_SEVaNLTJbbcWvazO8wfRKMznhWVZ_ydAdb0xiAq89M8fZ3Yx'

if ',' in categories:
    categories = [category.strip().lower() for category in categories.split(',')]
else:
    categories = categories.split()

search_info = {
    'term': term,
    'location': location,
    'categories': categories,
    'api_key': api_key
}


if 'current_action' not in st.session_state:
    st.session_state.current_action = 'Scrape Site'

if st.session_state.current_action == 'Scrape Site':
    if 'scrape_button_session' not in st.session_state:
        st.session_state.scrape_button_session = False
    
    def set_button_session():
        st.session_state.scrape_button_session = True

    if (st.button('Scrape site', on_click=set_button_session) or st.session_state.scrape_button_session):
        st.session_state.current_action = 'Scrape Site'

        st.write('Scraping the website...')
        result = scrape_website(search_info)
        
        if result:
            st.write("Business Data:")
            st.write(result)
        else:
            st.write("No results found")

elif st.session_state.current_action == 'Generate CSV':
    st.session_state.current_action = 'Generate CSV'
    st.header("CSV File Generation")

st.cache_data.clear()
st.cache_resource.clear()