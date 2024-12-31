import os
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

    # Save the file
    file_path = os.path.join(upload_directory, file.filename)
    file.save(file_path)

    return jsonify({"message": "Upload successful!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
