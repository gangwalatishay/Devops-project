from flask import Flask, request, jsonify
import joblib
from pyngrok import ngrok
from IPython.display import display, HTML

# Load the trained model
model = joblib.load('logistic_regression_model.pkl')

app = Flask(__name__)

@app.route('/')
def home():
    # HTML form to take inputs
    html_form = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Titanic Survival Prediction</title>
    <style>
        :root {
            --background-color-light: #f4f4f9; /* Light background color */
            --text-color-light: #333; /* Dark text color */
            --form-background-light: rgba(255, 255, 255, 0.95); /* Light background for form */
            --input-background-light: rgba(255, 255, 255, 0.1); /* Light background for inputs */
            --button-background-light: #2c3e50; /* Dark blue button */
            --button-color-light: #fff; /* White text */
            --notification-background-light: #333; /* Dark background for notification */
            --notification-color-light: #fff; /* White text */
            --border-color-light: #ddd; /* Light border color */

            --background-color-dark: #222; /* Dark background color */
            --text-color-dark: #ddd; /* Light text color */
            --form-background-dark: rgba(30, 30, 30, 0.95); /* Dark background for form */
            --input-background-dark: #444; /* Dark background for inputs */
            --button-background-dark: #2c3e50; /* Dark blue button */
            --button-color-dark: #fff; /* White text */
            --notification-background-dark: #333; /* Dark background for notification */
            --notification-color-dark: #fff; /* White text */
            --border-color-dark: #555; /* Dark border color */

            --background-color-custom: #e8f0ff; /* Custom background color */
        }

        body {
            background-color: var(--background-color-light);
            color: var(--text-color-light);
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 20px;
            margin: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            position: relative;
            transition: background-color 0.3s, color 0.3s;
        }
        h1 {
            margin-bottom: 20px;
        }
        #predictionForm {
            width: 90%;
            max-width: 400px;
            background-color: var(--form-background-light);
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: left;
            margin-bottom: 20px;
            transition: background-color 0.3s;
        }
        #predictionForm label {
            display: block;
            margin-bottom: 8px;
            color: var(--text-color-light);
        }
        #predictionForm input[type="text"] {
            width: calc(100% - 20px);
            padding: 10px;
            margin-bottom: 15px;
            border: none;
            border-radius: 6px;
            background-color: var(--input-background-light);
            color: var(--text-color-light);
            outline: none;
            transition: border-color 0.3s, background-color 0.3s;
        }
        #predictionForm input[type="text"]:focus {
            border: 1px solid var(--border-color-light);
        }
        #predictionForm button {
            width: 100%;
            padding: 12px;
            background-color: var(--button-background-light);
            color: var(--button-color-light);
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        #predictionForm button:hover {
            background-color: #1a252f; /* Darker shade on hover */
        }
        .notification {
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background-color: var(--notification-background-light);
            color: var(--notification-color-light);
            padding: 10px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            display: none;
            transition: background-color 0.3s, color 0.3s;
        }

        @media (prefers-color-scheme: dark) {
            body {
                background-color: var(--background-color-dark);
                color: var(--text-color-dark);
            }
            #predictionForm {
                background-color: var(--form-background-dark);
            }
            #predictionForm label {
                color: var(--text-color-dark);
            }
            #predictionForm input[type="text"] {
                background-color: var(--input-background-dark);
                color: var(--text-color-dark);
            }
            #predictionForm input[type="text"]:focus {
                border: 1px solid var(--border-color-dark);
            }
            #predictionForm button {
                background-color: var(--button-background-dark);
                color: var(--button-color-dark);
            }
            .notification {
                background-color: var(--notification-background-dark);
                color: var(--notification-color-dark);
            }
        }
    </style>
</head>
<body>
    <h1>Titanic Survival Prediction</h1>
    <form id="predictionForm">
        <label for="pclass">Pclass:</label>
        <input type="text" id="pclass" name="pclass" required><br><br>

        <label for="sex">Sex (0 for male, 1 for female):</label>
        <input type="text" id="sex" name="sex" required><br><br>

        <label for="age">Age:</label>
        <input type="text" id="age" name="age" required><br><br>

        <label for="sibsp">SibSp:</label>
        <input type="text" id="sibsp" name="sibsp" required><br><br>

        <label for="parch">Parch:</label>
        <input type="text" id="parch" name="parch" required><br><br>

        <label for="fare">Fare:</label>
        <input type="text" id="fare" name="fare" required><br><br>

        <label for="embarked">Embarked (0 for S, 1 for C, 2 for Q):</label>
        <input type="text" id="embarked" name="embarked" required><br><br>

        <button type="button" onclick="predictSurvival()">Predict</button>
    </form>

    <div id="notification" class="notification"></div>

    <script>
        function predictSurvival() {
            var xhr = new XMLHttpRequest();
            var url = "/predict";
            var data = new FormData(document.getElementById("predictionForm"));

            xhr.open("POST", url, true);
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);
                    var notification = document.getElementById("notification");
                    notification.style.display = "block";
                    notification.textContent = "Survival Prediction: " + response.prediction;

                    // Hide notification after 5 seconds
                    setTimeout(function() {
                        notification.style.display = "none";
                    }, 5000);
                }
            };
            xhr.send(data);
        }

        // Detect user's color scheme preference
        var prefersDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        if (prefersDarkMode) {
            document.documentElement.setAttribute('data-theme', 'dark');
        }
    </script>
</body>
</html>




    """
    return html_form

@app.route('/predict', methods=['POST'])
def predict():
    # Access form data
    pclass = request.form['pclass']
    sex = request.form['sex']
    age = request.form['age']
    sibsp = request.form['sibsp']
    parch = request.form['parch']
    fare = request.form['fare']
    embarked = request.form['embarked']

    # Convert data to appropriate types
    pclass = int(pclass)
    sex = int(sex)
    age = float(age)
    sibsp = int(sibsp)
    parch = int(parch)
    fare = float(fare)
    embarked = int(embarked)

    # Make prediction
    features = [[pclass, sex, age, sibsp, parch, fare, embarked]]
    prediction = model.predict(features)[0]

    return jsonify({'prediction': int(prediction)})

def run_flask_app():
    # Run Flask app on port 5000
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)

# Start ngrok tunnel
public_url = ngrok.connect(addr="5000", proto="http")
print("Public URL:", public_url)

# Display ngrok tunnel URL
display(HTML(f"<h2>Open this link in your browser to access the application:</h2><p>{public_url}</p>"))

try:
    # Keep the Flask app running
    run_flask_app()
except KeyboardInterrupt:
    # Shutdown ngrok and Flask app
    ngrok.kill()
