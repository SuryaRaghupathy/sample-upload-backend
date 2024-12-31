import os
import csv
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for communication with React frontend

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    # Ensure the uploads directory exists
    upload_directory = "./uploads"
    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)

    # Save the uploaded file
    file_path = os.path.join(upload_directory, file.filename)
    file.save(file_path)

    # Read and process the CSV file
    try:
        csv_data = []
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                csv_data.append(row)
        print(csv_data)
        # Return the CSV data as JSON
        return jsonify({"message": "Upload successful!", "data": csv_data}), 200

    except Exception as e:
        return jsonify({"message": "Failed to process the CSV file", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
