import os
import csv
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize the Flask application
app = Flask(__name__)
CORS(app)

# Directory to save uploaded files
UPLOAD_DIRECTORY = "uploads"

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the CSV upload API!"})

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the file part is in the request
    if 'file' not in request.files:
        return jsonify({"message": "No file part in the request"}), 400

    file = request.files['file']

    # Check if a file is selected
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    # Ensure the upload directory exists
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

    try:
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        file.save(file_path)

        # Read and process the CSV file
        csv_data = []
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                csv_data.append(row)

        # Return the CSV data as JSON
        return jsonify({"message": "Upload successful!", "data": csv_data}), 200

    except Exception as e:
        return jsonify({"message": "Failed to process the CSV file", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
