from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)  # Enable CORS on all routes

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload', methods=['POST'])

def upload_video():
    print('HI!')
    response = jsonify({"prediction": 'prediction'})
    return response, 200
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Make prediction
        prediction = True

        return jsonify({"prediction": prediction}), 200

    return jsonify({"error": "File not allowed"}), 400


if __name__ == '__main__':
    app.run(debug=True)
