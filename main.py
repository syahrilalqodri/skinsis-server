# Import library
import os
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

from PIL import Image
from io import BytesIO

from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array


# Flask Object 
app = Flask(__name__)

ALLOW_EXTENSION = {'jpg','jpeg'}

# Load the Machine Learning Model
model = tf.keras.models.load_model('model1_mobilenet.h5',custom_objects={'KerasLayer':hub.KerasLayer})

# Function to allow files format
def allow_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOW_EXTENSION

# Function to read the images
def read_image(image):
    img = Image.open(BytesIO(image))
    img = img.resize((150, 150), Image.ANTIALIAS)
    img = img_to_array(img)
    img /= 255
    img = np.expand_dims(img, axis=0)
    return img

# Server test function
@app.route('/') 
def index():
    return "skinsis"

# Route Predict Images
@app.route('/predict', methods=['POST'])
def predict():
    image = request.files['image']

    if image and allow_file(image.filename):
        image = image.read()
        img = read_image(image)
        results = model.predict(img)
        max_value = np.max(results)

        if max_value <= 0.08:
            resp = jsonify({'message': 'Image can not be predicted'})
            resp.status_code = 400
            return resp 
        elif max_value > 0.08:
            result = np.argmax(results, axis = 1)

            if result == 0:
                Name = "Acne and Rosacea" +" ({:.0%})".format(max_value)
                Recommendation = "14.92 gram"
            elif result == 1:
                Name = "Eczema" +" ({:.0%})".format(max_value)
            elif result == 2:
                Name = "Herpes HPV" +" ({:.0%})".format(max_value)
            elif result == 3:
                Name = "Psoriasis pictures Lichen Planus" +" ({:.0%})".format(max_value)
            elif result == 4:
                Name = "Seborrheic Keratoses" +" ({:.0%})".format(max_value)
            return jsonify({'Name' : Name, 'Recommendation' : Recommendation})
        else:
            res = jsonify({'message': 'Image extension is not allowed'})
            res.code_status = 400
            return res

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)),host='0.0.0.0',debug=True)



