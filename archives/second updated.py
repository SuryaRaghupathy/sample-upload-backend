# import os
# import csv
# import json
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import logging
# import random
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.common.exceptions import NoSuchElementException

# app = Flask(__name__)
# CORS(app)  # Enable CORS for communication with React frontend

# # Set up logging
# logging.basicConfig(filename="debug.log", level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s')

# def random_delay():
#     """Introduce a random delay to mimic human behavior."""
#     time.sleep(random.uniform(2, 5))

# def simulate_realistic_interaction(driver):
#     """Simulate realistic user interactions with error handling."""
#     try:
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(random.uniform(1, 3))
#         actions = ActionChains(driver)
#         actions.move_by_offset(random.randint(0, 50), random.randint(0, 50)).perform()
#     except Exception as e:
#         logging.error(f"Error during interaction simulation: {e}")

# def restart_browser():
#     """Restart the browser to prevent IP blocking issues."""
#     try:
#         options = webdriver.ChromeOptions()
#         # options.add_argument('--headless')
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')
#         return webdriver.Chrome(options=options)
#     except Exception as e:
#         logging.error(f"Error restarting browser: {e}")
#         return None

# @app.route('/')
# def home():
#     return "Hello, World!"

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({"message": "No file part in the request"}), 400

#     file = request.files['file']

#     if file.filename == '':
#         return jsonify({"message": "No selected file"}), 400

#     # Ensure the uploads directory exists
#     upload_directory = "./uploads"
#     if not os.path.exists(upload_directory):
#         os.makedirs(upload_directory)

#     # Save the uploaded file
#     file_path = os.path.join(upload_directory, file.filename)
#     file.save(file_path)

#     # Read and process the CSV file
#     try:
#         csv_data = []
#         with open(file_path, mode='r', encoding='utf-8') as csvfile:
#             csv_reader = csv.DictReader(csvfile)
#             for row in csv_reader:
#                 csv_data.append(row)

#         # Filter the data
#         filtered_data = [entry for entry in csv_data if entry.get("Keyword") and entry.get("Brand") and entry.get("Branch")]

#         if not filtered_data:
#             raise ValueError("No valid rows found in the CSV. Ensure 'Keyword', 'Brand', and 'Branch' columns are properly filled.")

#         # Initialize Selenium WebDriver
#         driver = restart_browser()
#         if not driver:
#             raise RuntimeError("Failed to initialize the Selenium WebDriver.")

#         try:
#             for idx, entry in enumerate(filtered_data):
#                 # Restart browser every 10 iterations to prevent blocking
#                 if idx > 0 and idx % 10 == 0:
#                     driver.quit()
#                     driver = restart_browser()
#                     if not driver:
#                         raise RuntimeError("Failed to restart the Selenium WebDriver.")

#                 keyword = entry["Keyword"]
#                 brand = entry["Brand"]
#                 branch = entry["Branch"]

#                 # Open Google UK
#                 driver.get("https://www.google.co.uk/?gl=uk")
#                 random_delay()

#                 # Perform search
#                 try:
#                     search_bar = driver.find_element(By.NAME, "q")
#                     search_bar.clear()
#                     search_bar.send_keys(keyword)
#                     search_bar.send_keys(Keys.RETURN)
#                     random_delay()
#                 except NoSuchElementException as e:
#                     logging.error(f"Search bar not found for keyword '{keyword}': {e}")
#                     continue

#                 try:
#                     # Extract Maps link
#                     maps_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Maps")
#                     maps_url = maps_link.get_attribute("href")

#                     driver.get(maps_url)
#                     random_delay()

#                     # Scroll and extract ranking list
#                     scrollable_div = driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
#                     last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)

#                     while True:
#                         driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
#                         time.sleep(random.uniform(2, 5))
#                         new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
#                         if new_height == last_height:
#                             break
#                         last_height = new_height

#                     elements = driver.find_elements(By.CLASS_NAME, "qBF1Pd.fontHeadlineSmall")
#                     extracted_texts = [element.text for element in elements]
#                     entry["ranking_list"] = extracted_texts

#                     # Find brand and branch position
#                     entry["position"] = None
#                     for index, element in enumerate(extracted_texts):
#                         if brand in element and branch in element:
#                             entry["position"] = index + 1
#                             break
#                 except Exception as e:
#                     logging.error(f"Error extracting rankings for keyword '{keyword}': {e}")
#                     entry["ranking_list"] = []
#                     entry["position"] = None
                    

#                     # Print each ranking list and position
#                     print(f"Keyword: {keyword}")
#                     print(f"Ranking List: {entry['ranking_list']}")
#                     print(f"Position: {entry['position']}")

#         finally:
#             driver.quit()

#         # Return the CSV data as JSON
#         return jsonify({"message": "Upload successful!", "data": filtered_data}), 200

#     except Exception as e:
#         logging.error(f"Failed to process the CSV file: {e}")
#         return jsonify({"message": "Failed to process the CSV file", "error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)
