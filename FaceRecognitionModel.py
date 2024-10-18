import os
import cv2
import numpy as np
import base64
import logging
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, Blueprint
from deepface import DeepFace  # Import DeepFace for face recognition
from models import PredictionHistory


# Initialize app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management
app2 = Blueprint('app2', __name__)  # Create a blueprint

# Setup for camera and uploads folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Set logging
logging.basicConfig(level=logging.DEBUG)

# Set the threshold value for face recognition accuracy
THRESHOLD = 0.2

# Function to save the image in the filesystem
def save_image(username, image_data):
    try:
        image_bytes = base64.b64decode(image_data.split(",")[1])
        image_path = os.path.join(UPLOAD_FOLDER, f"{username}.jpg")
        with open(image_path, 'wb') as f:
            f.write(image_bytes)
        return image_path
    except Exception as e:
        logging.error(f"Error saving image: {e}")
        return None

# Authenticate the user's face
def authenticate_user(image_data):
    try:
        # Decode the base64 image data
        image_bytes = base64.b64decode(image_data.split(",")[1])
        image_array = np.frombuffer(image_bytes, dtype=np.uint8)
        signin_image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        most_similar_user_image = None
        most_similar_user_image_filename = None
        min_distance = float('inf')

        # Loop through saved images and compare with the sign-in image
        for filename in os.listdir(UPLOAD_FOLDER):
            if filename.endswith(".jpg"):
                user_image_path = os.path.join(UPLOAD_FOLDER, filename)
                try:
                    # Compare the sign-in image with the user images
                    result = DeepFace.verify(img1_path=signin_image, img2_path=user_image_path, enforce_detection=False)
                    distance = result['distance']
                    print(f"Comparing with {filename}: distance = {distance}, accuracy = {(1 - distance) * 100}%")  # Debugging line
                    
                    if distance < min_distance:
                        min_distance = distance
                        most_similar_user_image = user_image_path
                        most_similar_user_image_filename = filename
                except Exception as e:
                    logging.error(f"Error processing {filename}: {e}")
                    continue

        # Calculate accuracy
        accuracy = (1 - min_distance) * 100 if min_distance != float('inf') else 0  # Ensure accuracy is computed correctly
        
        # Extract username (assuming the username is derived from the filename)
        username = most_similar_user_image_filename.split('.')[0] if most_similar_user_image_filename else None
        
        # Use username as user_national_id if they are the same
        user_national_id = username
        
        # Return four values including the user_national_id
        return most_similar_user_image, most_similar_user_image_filename, accuracy, user_national_id

    except Exception as e:
        logging.error(f"Error in authenticate_user: {e}")
        return None, None, None, None



# Function to initialize the SQLite database
def init_db():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        image BLOB NOT NULL
    )''')
    conn.commit()
    conn.close()

# Function to save user data in the database
def save_user_data(username, image_data):
    try:
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        image_binary = base64.b64decode(image_data.split(',')[1])
        cursor.execute('''INSERT INTO users (username, image) VALUES (?, ?)''', (username, image_binary))
        conn.commit()
        return True
    except Exception as e:
        logging.error(f"Error saving user data: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

# Route for sign-up
@app2.route('/signupuser', methods=['GET', 'POST'])
def signupuser():
    if request.method == 'POST':
        username = request.form.get('username')
        image_data = request.form.get('image')

        # Check if image data is provided
        if not image_data:
            return jsonify({"message": "No image data received. Please provide a valid image.", "status": 400}), 400

        # Authenticate user by face recognition
        most_similar_user_image, similar_image_filename, accuracy, existing_user_national_id = authenticate_user(image_data)

        # Check if the accuracy is below the threshold (sign-up condition)
        if accuracy < 50.0:  # If accuracy is less than 50%
            # Save user image and data
            try:
                # Save the new user's image
                image_path = save_image(username, image_data)
                if image_path:
                    # Save the user's data to the database or file
                    saved = save_user_data(username, image_data)
                    if saved:
                        return jsonify({"message": "Signed up successfully!", "status": 200}), 200
                    else:
                        return jsonify({"message": "Failed to save user data to the database", "status": 500}), 500
                else:
                    return jsonify({"message": "Failed to save user image", "status": 500}), 500
            except Exception as e:
                logging.error(f"Exception during signup: {e}")
                return jsonify({"message": "An error occurred during sign-up. Please try again.", "status": 500}), 500

        # If accuracy is greater than or equal to 50%
        return jsonify({
            "message": f"Accuracy: {round(float(accuracy), 2)}% is above the required threshold. Please sign in instead.",
            "accuracy": round(float(accuracy), 2),
            "status": 401
        }), 401

    # Render the sign-up form for GET requests
    return render_template('signup.html')  # Ensure this template exists



@app2.route('/signin', methods=['POST'])
def signinuser():
    if request.method == 'POST':
        try:
            logging.info("Signin request received.")
            image_data = request.form.get('image')
            logging.info(f"Received image data: {image_data}")

            if not image_data:
                return jsonify({"message": "No image data received. Please provide a valid image.", "status": 400}), 400

            most_similar_user_image_path, similar_image_filename, accuracy, user_national_id = authenticate_user(image_data)

            if most_similar_user_image_path:
                logging.info(f"Computed accuracy: {accuracy:.2f}%")
                
                # Check if the accuracy is below 80%
                if accuracy < 70.0:  # If accuracy is less than 80%
                    return jsonify({
                        "message": f"Authentication failed. Accuracy: {round(float(accuracy), 2)}% is below the required threshold.",
                        "accuracy": round(float(accuracy), 2),
                        "status": 401
                    }), 401
                
                # If accuracy is 80% or higher
                logging.info(f"User authenticated with {accuracy:.2f}% accuracy.")
                session['user_id'] = user_national_id  # Store user ID in session

                return jsonify({
                    "message": f"Authentication successful. Accuracy: {round(float(accuracy), 2)}%",
                    "status": 200,
                    "model_link": url_for('app1.select_model')  # Link to try models
                }), 200

            return jsonify({"message": "Authentication failed. No similar user image found.", "status": 401}), 401

        except Exception as e:
            logging.error(f"Error during sign-in: {e}")
            return jsonify({"message": f"An error occurred: {e}", "status": 500}), 500


@app2.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('signinpage'))  # Redirect if not signed in

    user_id = session['user_id']  # Get user_id from session
    predictions = PredictionHistory.query.filter_by(user_id=user_id).all()  # Query history

    return render_template('history.html', predictions=predictions)  # Render a history template


# User profile page
@app2.route('/user_profile', methods=['GET'])
def user_profile():
    if 'username' in session:
        return render_template('profile.html', username=session['username'])
    return redirect(url_for('app2.signinpage'))


# Basic routes
@app2.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app2.route('/signin', methods=['GET'])
def signinpage():
    return render_template('signin.html')

@app2.route('/signup', methods=['GET'])
def signuppage():
    return render_template('signup.html')

# Register the blueprint
app.register_blueprint(app2)

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True, port=5002)
