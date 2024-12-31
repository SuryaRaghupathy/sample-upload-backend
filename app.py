from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for communication with React frontend

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part in the request"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    # Save the file to a desired location (optional)
    file.save(f"./uploads/{file.filename}")

    return jsonify({"message": "Upload successful!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
