import os
import tensorflow as tf
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from prediction import predict
from config import BASE_LEARNERS, META_CLASSIFIER

app = Flask(__name__)
CORS(app)  # Enable CORS on all routes

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov'}

inception_optical = tf.keras.models.load_model(BASE_LEARNERS[0])
dense_optical = tf.keras.models.load_model(BASE_LEARNERS[1])
xception_lbp = tf.keras.models.load_model(BASE_LEARNERS[2])
dense_lbp = tf.keras.models.load_model(BASE_LEARNERS[3])

meta_classifier = tf.keras.models.load_model(META_CLASSIFIER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.before_request
def before_request():
    print('Before request!')
    headers = {'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
               'Access-Control-Allow-Headers': 'Content-Type'}
    if request.method.lower() == 'options':
        return jsonify(headers), 200


@app.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Make prediction
        prediction = predict(filepath, inception_optical, dense_optical, xception_lbp, dense_lbp, meta_classifier)
        print('prediction made')

        return jsonify({"prediction": prediction}), 200

    return jsonify({"error": "File not allowed"}), 400


if __name__ == '__main__':
    app.run(debug=True)
