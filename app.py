from flask import Flask, request, jsonify
from fetcher import fetch_student_data
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests (from mobile, browser, etc.)

@app.route('/')
def home():
    return jsonify({"message": "HICAS Attendance API is running."})

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        roll = data.get("roll")
        password = data.get("password")
        dob = data.get("dob")

        # Validate input
        if not all([roll, password, dob]):
            return jsonify({"status": "fail", "message": "Missing required fields"}), 400

        # Call the Selenium fetcher
        result = fetch_student_data(roll, password, dob)

        # Check fetcher response
        if result.get("status") != "success":
            return jsonify(result), 500

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"status": "fail", "message": f"API error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render passes PORT as an environment variable
    app.run(host="0.0.0.0", port=port)
