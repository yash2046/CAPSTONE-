from flask import Flask, request, jsonify, render_template
import os
import cv2
import numpy as np
from tensorflow import keras
import base64

app = Flask(__name__)

model = keras.models.load_model('./stock_candle_ai_model.h5')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process_image", methods=["POST"])
def process_image():
    try:
        uploaded_image = request.files['image']

        if uploaded_image and allowed_file(uploaded_image.filename):
            image_path = os.path.join(os.getcwd(), uploaded_image.filename)
            uploaded_image.save(image_path)

            img = cv2.imread(image_path)
            img = cv2.resize(img, (224, 224))
            img = np.expand_dims(img, axis=0)

            prediction = model.predict(img)

            if prediction > 0.5:
                result = "up"
            else:
                result = "down"

            _, buffer = cv2.imencode(".png", img[0])
            img_base64 = base64.b64encode(buffer).decode("utf-8")

            return jsonify({"image": img_base64, "result": result})
        else:
            return jsonify({"image": "", "result": "Invalid image file"})

    except Exception as e:
        return jsonify({"image": "", "result": f"Error: {str(e)}"})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}

if __name__ == "__main__":
    app.run(debug=True, port=8080)
