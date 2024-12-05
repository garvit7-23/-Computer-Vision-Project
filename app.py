import os
import sqlite3
import logging
from flask import Flask, render_template, request, jsonify
from twilio.rest import Client
from inference_sdk import InferenceHTTPClient

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
logging.basicConfig(level=logging.DEBUG)

# Roboflow API details
ROBOFLOW_API_URL = "https://detect.roboflow.com"
ROBOFLOW_API_KEY = "FbVisiqX6WHL2luxwITs"  # Replace with your API key

# Twilio details for SMS notifications
TWILIO_ACCOUNT_SID = "VAf0734fb0c4aa6b1d58c7a21c06d26a96"
TWILIO_AUTH_TOKEN = "03e6223a6d33ed2ffbeab2050e9f0006"
TWILIO_PHONE_NUMBER = "+17755874164"

# Penalty increment amount
PENALTY_INCREMENT = 100  # Penalty per litter detection

# Database initialization
DB_FILE = "vehicles.db"
if not os.path.exists(DB_FILE):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE vehicles (
                plate TEXT PRIMARY KEY,
                count INTEGER DEFAULT 0,
                penalty INTEGER DEFAULT 0
            )
        ''')

# Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Roboflow Inference client
client = InferenceHTTPClient(
    api_url=ROBOFLOW_API_URL,
    api_key=ROBOFLOW_API_KEY
)

def send_notification(plate, penalty):
    """Send notification to vehicle owners."""
    message = f"Dear vehicle owner, littering has been detected from your vehicle {plate}. Current penalty: ${penalty}."
    twilio_client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to="+919914145873" 
    )

@app.route('/')
def home():
    return render_template('index.html')  # Frontend for image upload

@app.route('/detect', methods=['POST'])
def detect_litter():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save the uploaded file to a temporary path
    temp_path = os.path.join("temp", file.filename)
    os.makedirs("temp", exist_ok=True)
    file.save(temp_path)

    try:
        # Upload the saved image to Roboflow
        result = client.run_workflow(
            workspace_name="garvit-mhbou",  
            workflow_id="text-recognition-agn", 
            images={
                "image": temp_path  # Pass the file path instead of raw data
            }
        )
        print(result)

        if not result:
            return jsonify({"error": "Detection failed"}), 500
        result_data = result[0] if isinstance(result, list) else result
        # Process the detection result
        detections = result_data.get("predictions", [])
        for detection in detections:
            if detection["class"] == "license_plate":
                plate = detection["ocr_text"]

                # Update vehicle record in the database
                with sqlite3.connect(DB_FILE) as conn:
                    cur = conn.cursor()
                    cur.execute("SELECT count, penalty FROM vehicles WHERE plate = ?", (plate,))
                    record = cur.fetchone()

                    if record:
                        count, penalty = record
                        count += 1
                        penalty += PENALTY_INCREMENT
                        cur.execute("UPDATE vehicles SET count = ?, penalty = ? WHERE plate = ?", (count, penalty, plate))
                    else:
                        count = 1
                        penalty = PENALTY_INCREMENT
                        cur.execute("INSERT INTO vehicles (plate, count, penalty) VALUES (?, ?, ?)", (plate, count, penalty))

                # Send notification
                send_notification(plate, penalty)

                return jsonify({"plate": plate, "count": count, "penalty": penalty})

        return jsonify({"message": "No license plate detected"}), 404

    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.route('/records', methods=['GET'])
def get_records():
    """Fetch all vehicle records."""
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM vehicles")
        records = cur.fetchall()
    return jsonify(records)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

