import os
import csv
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import random
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS for communication with React frontend

# Set upload size limit to 16 MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Set up logging
logging.basicConfig(filename="debug.log", level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s')

def restart_browser():
    """Restart the browser to prevent IP blocking issues."""
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        return webdriver.Chrome(options=options)
    except Exception as e:
        logging.error(f"Error restarting browser: {e}")
        return None

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/test-webdriver', methods=['GET'])
def test_webdriver():
    """Test the Selenium WebDriver functionality."""
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.google.co.uk")
        title = driver.title
        driver.quit()
        return jsonify({"message": "WebDriver test successful!", "title": title}), 200
    except Exception as e:
        logging.error(f"Error testing WebDriver: {e}")
        return jsonify({"message": "WebDriver test failed", "error": str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({"message": "Only CSV files are allowed"}), 400

    # Ensure the uploads directory exists
    upload_directory = "./uploads"
    if not os.path.exists(upload_directory):
        try:
            os.makedirs(upload_directory)
        except Exception as e:
            logging.error(f"Failed to create upload directory: {e}")
            return jsonify({"message": "Failed to create upload directory"}), 500

    # Save the uploaded file
    file_path = os.path.join(upload_directory, secure_filename(file.filename))
    file.save(file_path)

    # Read and process the CSV file
    try:
        csv_data = []
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                csv_data.append(row)

        # Return the CSV data as JSON
        return jsonify({"message": "Upload successful!", "data": csv_data}), 200

    except Exception as e:
        logging.error(f"Failed to process the CSV file: {e}")
        return jsonify({"message": "Failed to process the CSV file", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
