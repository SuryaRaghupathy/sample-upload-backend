from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

def initialize_webdriver():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems in containerized environments

    # Initialize the WebDriver using ChromeDriverManager to handle driver binaries
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver

@app.route('/get-title', methods=['GET'])
def get_title():
    driver = initialize_webdriver()
    driver.get("https://www.google.com")
    title = driver.title
    driver.quit()
    return jsonify({"title": title})

if __name__ == "__main__":
    app.run(debug=True)
