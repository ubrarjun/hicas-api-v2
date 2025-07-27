# app.py

from flask import Flask, request, jsonify
from fetcher import fetch_student_data
from flask_cors import CORS
import os  # ✅ Needed for dynamic PORT binding on Render

app = Flask(__name__)
CORS(app)  # allows Android app (or browser) to access from anywhere

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

        if not all([roll, password, dob]):
            return jsonify({"status": "fail", "message": "Missing required fields"}), 400

        result = fetch_student_data(roll, password, dob)

        # If fetcher itself returns an error
        if result.get("status") != "success":
            return jsonify(result), 500

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"status": "fail", "message": f"API error: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # ✅ Use Render's assigned port if available
    app.run(host="0.0.0.0", port=port)
