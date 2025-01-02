from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from flask_cors import CORS
import logging
import traceback
import platform

app = Flask(__name__)
CORS(app)

# Logging setup
logging.basicConfig(level=logging.DEBUG)


def initialize_webdriver():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )

        # Dynamically manage the Chrome binary location for different systems (optional)
        def get_chrome_binary_path():
            system_name = platform.system()
            if system_name == "Windows":
                return r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            elif system_name == "Linux":
                return "/usr/bin/google-chrome"
            elif system_name == "Darwin":  # macOS
                return "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            else:
                raise Exception(f"Unsupported OS: {system_name}")

        # Optional: Uncomment the next line if needed to set Chrome binary path
        # chrome_options.binary_location = get_chrome_binary_path()

        # Use WebDriverManager to handle ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        logging.info("WebDriver initialized successfully.")
        return driver
    except Exception as e:
        logging.error(f"Error initializing WebDriver: {e}")
        logging.error(traceback.format_exc())
        raise


@app.route('/get-title', methods=['GET'])
def get_title():
    try:
        driver = initialize_webdriver()
        url = "https://www.collinsonhall.co.uk/"
        logging.info(f"Fetching URL: {url}")
        driver.get(url)

        # Retrieve the page title
        title = driver.title
        logging.info(f"Page title fetched: {title}")

        driver.quit()
        return jsonify({"title": title})
    except Exception as e:
        logging.error(f"Error in /get-title: {e}")
        logging.error(traceback.format_exc())
        return jsonify({"error": "Failed to fetch title", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
