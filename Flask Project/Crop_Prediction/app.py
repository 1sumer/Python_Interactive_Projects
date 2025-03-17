from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load Model and Label Encoder
with open("models/classifier.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("models/label_encoder.pkl", "rb") as encoder_file:
    label_encoder = pickle.load(encoder_file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data from form
        input_features = np.array([[float(request.form['N']), float(request.form['P']),
                                    float(request.form['K']), float(request.form['temperature']),
                                    float(request.form['humidity']), float(request.form['ph']),
                                    float(request.form['rainfall'])]])

        # Predict crop (numeric value)
        prediction = model.predict(input_features)[0]

        # Convert numeric prediction back to crop name
        crop_name = label_encoder.inverse_transform([prediction])[0]

        return render_template('result.html', prediction=crop_name)
    except Exception as e:
        return render_template('index.html', error=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
