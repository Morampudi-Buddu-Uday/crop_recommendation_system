from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('C:\\Users\\uday\\Desktop\\Sumer_Intern\\Crop_recommendation (1).csv')

# Feature scaling
scaler = StandardScaler()
X = df.drop(['label'], axis=1)
y = df['label']
X_scaled = scaler.fit_transform(X)

# Train the model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_scaled, y)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        input_data = request.form.to_dict()
        input_data_array = [float(input_data['N']), float(input_data['P']), float(input_data['K']),
                            float(input_data['temperature']), float(input_data['humidity']),
                            float(input_data['ph']), float(input_data['rainfall'])]

        # Reshape the array
        reshaped_data = np.asarray(input_data_array).reshape(1, -1)

        # Standardize the data
        reshaped_data_transformed = scaler.transform(reshaped_data)

        # Make prediction
        prediction = model.predict(reshaped_data_transformed)

        return render_template('index.html', prediction=prediction[0])

if __name__ == '__main__':
    app.run(debug=True)
