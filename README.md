# Litter Detection System

## Overview
The Litter Detection System is an AI-powered application designed to identify littering incidents through uploaded images. It detects license plates of vehicles involved in littering, logs the information in a database, and sends SMS notifications to vehicle owners about penalties. This project leverages Roboflow for object detection, SQLite for data storage, and Twilio for SMS notifications.

## Features
- Detects license plates from uploaded images.
- Maintains a database of vehicle records, including detection count and penalties.
- Sends SMS notifications to vehicle owners about littering penalties.
- Provides an interactive web interface for image uploads and viewing vehicle records.

## Technologies Used
- **Flask**: Backend framework for handling API requests.
- **Roboflow**: AI-powered object detection and OCR.
- **SQLite**: Lightweight database for storing vehicle records.
- **Twilio**: SMS service for notifications.
- **HTML/CSS/JavaScript**: Frontend for user interaction.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/litter-detection-system.git
   cd litter-detection-system
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python
   >>> import sqlite3
   >>> conn = sqlite3.connect('vehicles.db')
   >>> conn.execute('''
       CREATE TABLE vehicles (
           plate TEXT PRIMARY KEY,
           count INTEGER DEFAULT 0,
           penalty INTEGER DEFAULT 0
       )
   ''')
   >>> conn.close()
   ```

5. Update configuration variables in `app.py`:
   - `ROBOFLOW_API_KEY`: Replace with your Roboflow API key.
   - `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, and `TWILIO_PHONE_NUMBER`: Replace with your Twilio credentials.

6. Run the application:
   ```bash
   python app.py
   ```

7. Open the web interface:
   - Visit `http://127.0.0.1:5000` in your browser.

## Usage
1. Upload an image in the "Upload Image" section to detect littering incidents.
2. View detected vehicle details and penalties.
3. Use the "Show Records" button to view all stored vehicle records.

## Project Structure
```
.
├── app.py            # Main application logic
├── templates/        # HTML templates
│   └── index.html
├── static/
│   ├── styles.css    # CSS for styling
├── vehicles.db       # SQLite database file
├── requirements.txt  # Python dependencies
└── README.md         # Project documentation
```

## API Endpoints

### `POST /detect`
- **Description**: Accepts an image file for litter detection.
- **Request**:
  - Form-data with the key `file` containing the image.
- **Response**:
  - Success: JSON with vehicle details (`plate`, `count`, `penalty`).
  - Failure: JSON with an error message.

### `GET /records`
- **Description**: Retrieves all stored vehicle records.
- **Response**:
  - Success: JSON array of vehicle records.



