from flask import Flask, request, jsonify
import joblib
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Load the trained model
model = joblib.load('logistic_regression_model.pkl')

# Initialize Flask app
app = Flask(__name__)

# HTML form for user inputs
@app.route('/')
def home():
    html_form = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Titanic Survival Prediction</title>
        <style>
            body {
                background-color: #f4f4f9;
                color: #333;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 20px;
            }
            #predictionForm {
                max-width: 400px;
                margin: auto;
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            #predictionForm label {
                display: block;
                margin-bottom: 8px;
            }
            #predictionForm input {
                width: 100%;
                padding: 10px;
                margin-bottom: 15px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            #predictionForm button {
                background-color: #2c3e50;
                color: #fff;
                padding: 10px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            #predictionForm button:hover {
                background-color: #1a252f;
            }
        </style>
    </head>
    <body>
        <h1>Titanic Survival Prediction</h1>
        <form id="predictionForm" method="post" action="/predict">
            <label for="pclass">Pclass:</label>
            <input type="text" id="pclass" name="pclass" required><br>

            <label for="sex">Sex (0 for male, 1 for female):</label>
            <input type="text" id="sex" name="sex" required><br>

            <label for="age">Age:</label>
            <input type="text" id="age" name="age" required><br>

            <label for="sibsp">SibSp:</label>
            <input type="text" id="sibsp" name="sibsp" required><br>

            <label for="parch">Parch:</label>
            <input type="text" id="parch" name="parch" required><br>

            <label for="fare">Fare:</label>
            <input type="text" id="fare" name="fare" required><br>

            <label for="embarked">Embarked (0 for S, 1 for C, 2 for Q):</label>
            <input type="text" id="embarked" name="embarked" required><br>

            <button type="submit">Predict</button>
        </form>
    </body>
    </html>
    """
    return html_form

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract form data
        pclass = int(request.form['pclass'])
        sex = int(request.form['sex'])
        age = float(request.form['age'])
        sibsp = int(request.form['sibsp'])
        parch = int(request.form['parch'])
        fare = float(request.form['fare'])
        embarked = int(request.form['embarked'])

        # Prepare features for prediction
        features = [[pclass, sex, age, sibsp, parch, fare, embarked]]
        prediction = model.predict(features)[0]

        # Return prediction result as JSON
        return jsonify({'prediction': int(prediction)})
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return jsonify({'error': 'Invalid input. Please check your data.'}), 400

# Run Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
