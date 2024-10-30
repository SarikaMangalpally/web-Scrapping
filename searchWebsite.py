import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote


# Function to scrape the official website URL for a given business title
def find_official_website(business_alias):
    url = f'https://www.yelp.com/biz/{business_alias}'
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        anchor_tags = soup.select('p.y-css-1o34y7f > a.y-css-8hdzny')
        url_match = None

        for tag in anchor_tags:
            href_value = tag['href']
            if 'url' in href_value:
                url_match = re.search(r'url=([^&]+)', href_value).group(1)
                break

        decoded_url = unquote(url_match)+'/' if url_match else ''
        return decoded_url
    except Exception as e:
        return f"An error occurred: {e}"


# title_to_search = "travelers-table-houston"  # Replace with your business title
# official_website = find_official_website(title_to_search)
# print(f"Official Website URL: {official_website}")