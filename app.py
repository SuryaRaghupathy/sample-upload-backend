import requests
from bs4 import BeautifulSoup
import time
import re
import json
import csv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# Retry strategy to handle timeouts and connection errors
retry_strategy = Retry(
    total=3,  # Number of retries
    backoff_factor=1,  # Wait time between retries (in seconds)
    status_forcelist=[429, 500, 502, 503, 504],  # Retry on these HTTP errors
    allowed_methods=["HEAD", "GET", "OPTIONS"]  # Corrected 'method_whitelist' to 'allowed_methods'
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)

http.mount("http://", adapter)

# Base URL
base_url = "https://www.fineandcountry.co.uk/sales/property-for-sale/united-kingdom?currency=INR&addOptions=sold&sortBy=price-high&country=GB&address=United+Kingdom&page="

# Dictionary to store all property information
property_data = {}

# Regular expression pattern to extract URL from style attribute
url_pattern = re.compile(r'url\((.*?)\)')

# Loop through all pagination pages
for page in range(1, 150):  # Adjust the range as needed
    url = base_url + str(page)
    try:
        response = http.get(url, timeout=10)  # Set a timeout to prevent hanging
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page}: {e}")
        continue

    # Check if the page request is successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all property divs with class "slide__media"
        property_divs = soup.find_all('div', class_='slide__media')

        # If no properties are found, stop the scraping (end of data)
        if not property_divs:
            print(f"No more properties found. Stopping at page {page}.")
            break

        # Find all author info divs with class "card__author-info"
        author_divs = soup.find_all('div', class_='card__author-info')

        # Loop through the divs and extract property URLs and background image URLs
        for idx, div in enumerate(property_divs):
            # Find the 'a' tag and extract the href attribute (property URL)
            link = div.find('a')['href']

            # Skip URLs with "javascript:void(0)"
            if link == "javascript:void(0)":
                continue

            full_url = link

            # Extract the corresponding branch location from author_divs
            if idx < len(author_divs):
                p_tag = author_divs[idx].find('p')
                branch_location = p_tag.get_text(strip=True) if p_tag else "N/A"
            else:
                branch_location = "N/A"

            # Find the slide image div and extract the background image URL from style attribute
            slide_image_div = div.find('div', class_='slide__image')
            if slide_image_div and 'style' in slide_image_div.attrs:
                style = slide_image_div['style']
                image_url_match = url_pattern.search(style)
                background_image_url = image_url_match.group(1) if image_url_match else "N/A"
            else:
                background_image_url = "N/A"

            # Now visit the property URL to extract the section__text and section__property-summary div content
            try:
                property_page_response = http.get(full_url, timeout=10)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching property URL {full_url}: {e}")
                continue

            if property_page_response.status_code == 200:
                property_page_soup = BeautifulSoup(property_page_response.text, 'html.parser')

                # Extract the section__text div content
                section_text_div = property_page_soup.find('div', class_='section__text')
                section_text = section_text_div.get_text(strip=True) if section_text_div else "N/A"

                # Extract the section__property-summary div content
                section_summary_div = property_page_soup.find('div', class_='section__property-summary')
                section_summary = section_summary_div.get_text(strip=True) if section_summary_div else "N/A"
            else:
                section_text = "N/A"
                section_summary = "N/A"

            # Store the data in the dictionary
            property_data[full_url] = {
                'full_url': full_url,
                'branch_location': branch_location,
                'background_image_url': background_image_url,
                'section_text': section_text,
                'section_summary': section_summary
            }

            # Print the stored data to the terminal
            print(f"Property URL: {full_url}, Branch Location: {branch_location}, Image URL: {background_image_url}, Section Text: {section_text}, Section Summary: {section_summary}")

        # Print progress
        print(f"Scraped page {page}")
    else:
        print(f"Failed to retrieve page {page}")

    # Add delay to avoid overloading the server
    time.sleep(2)

# Save the property data to a JSON file
with open('property_data.json', 'w') as json_file:
    json.dump(property_data, json_file, indent=4)

# Convert JSON data to CSV format
csv_columns = ['full_url', 'branch_location', 'background_image_url', 'section_text', 'section_summary']
csv_file = "property_data.csv"

try:
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for url, data in property_data.items():
            writer.writerow(data)
    print("Data successfully written to CSV file.")
except IOError:
    print("I/O error")

print("Scraping complete!")
