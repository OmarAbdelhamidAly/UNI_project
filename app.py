from flask import Flask, request, render_template, redirect, url_for, jsonify, Blueprint, session,flash
import os
from models import db, PredictionHistory  # Import your database instance and models
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)

# Set up the database URI and other configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'  # Specify your database URI here
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance

# Initialize the database with the Flask app
db.init_app(app)

# Create a Blueprint
app1 = Blueprint('app1', __name__)

# Load models
models = {
    'lung': load_model('inceptionv3_model_lung.h5'),
    'prain': load_model('inceptionv3_model_prain.h5'),
    'chest': load_model('InceptionV3_model_chest.h5'),
    'colon_lung': load_model('InceptionV3_model_lung_colon.h5'),
    'bone_marrow': load_model('DenseNet201_modell_bone_marrow.h5')
}

# Define the classes for each model
classes_lung = [
    'adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib', 
    'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa', 
    'normal', 
    'squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa'
]
classes_prain = ['1', '2', '3']
classes_chest = ['normal', 'pneumonia']
classes_colon_lung=['colon_aca', 'colon_n', 'lung_aca', 'lung_n', 'lung_scc']
classes_bone_marrow=['Benign', '[Malignant] early Pre-B', '[Malignant] Pre-B', '[Malignant] Pro-B']
    
@app1.route('/')
def index():
    if 'user_id' not in session:  # Check if user is logged in
        return redirect(url_for('app2.signinpage'))
    return render_template('index.html')


@app1.route('/select_model', methods=['GET', 'POST'])
def select_model():
    if 'user_id' not in session:  # Check if user is logged in
        return redirect(url_for('app2.signinpage'))

    if request.method == 'POST':
        selected_model = request.form.get('model')
        return redirect(url_for('app1.upload_file', model=selected_model))

    return render_template('select_model.html')  # Render the form again in case of GET

@app1.route('/history')
def history():
    if 'user_id' not in session:  # Ensure user is logged in
        return redirect(url_for('app2.signinpage'))
    
    # Query the prediction history for the logged-in user
    user_id = session['user_id']
    history_entries = PredictionHistory.query.filter_by(user_id=user_id).all()

    # Create a list of results to display
    history_data = []
    for entry in history_entries:
        history_data.append({
            'id': entry.id,
            'prediction': entry.prediction,
            'timestamp': entry.timestamp.strftime("%Y-%m-%d %H:%M")  # Format the timestamp
        })

    # Render the results on a page instead of JSON
    return render_template('history.html', predictions=history_data)

@app1.route('/doctor/history')
def doctor_history():
    # Check if the user is logged in
    if 'user_id' not in session:
        flash("Please log in to continue.", "warning")
        return redirect(url_for('app2.signinpage'))

    # Query all prediction history for all users (patients)
    history_entries = PredictionHistory.query.all()

    # Create a list of results to display
    history_data = []
    for entry in history_entries:
        history_data.append({
            'id': entry.id,
            'user_id': entry.user_id,  # Include user id to differentiate patients
            'prediction': entry.prediction,
            'timestamp': entry.timestamp.strftime("%Y-%m-%d %H:%M")  # Format the timestamp
        })

    # Render the results on a page for doctors
    return render_template('doctor_history.html', predictions=history_data)


    # Render the results on a page for doctors
    return render_template('doctor_history.html', predictions=history_data)
@app1.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "app1 is running"}), 200

@app1.route('/upload_file')
def upload_file():
    if 'user_id' not in session:  # Check if user is logged in
        return redirect(url_for('app2.signinpage'))
    model = request.args.get('model')
    return render_template('upload.html', model=model)


@app1.route('/upload', methods=['POST'])
def upload():
    if 'user_id' not in session:  # Check if user is logged in
        return redirect(url_for('app2.signinpage'))

    user_id = session['user_id']  # Get user_id from the session
    model_name = request.form.get('model')

    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400

    # Save the file to the uploads directory
    uploads_dir = 'uploads'
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)

    file_path = os.path.join(uploads_dir, file.filename)
    file.save(file_path)

    # Preprocess the image
    img = image.load_img(file_path, target_size=(224, 224))  # Adjust target size based on your model input
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array /= 255.0  # Normalize the image

    # Make prediction
    if model_name in models:
        predictions = models[model_name].predict(img_array)
        predicted_class_index = np.argmax(predictions, axis=1)[0]

        # Map the prediction index to class name
        if model_name == 'lung':
            result = classes_lung[predicted_class_index]
        elif model_name == 'prain':
            result = classes_prain[predicted_class_index]
        elif model_name == 'chest':
            result = classes_chest[predicted_class_index]
        elif model_name == 'bone_marrow':
            result = classes_bone_marrow[predicted_class_index]
        elif model_name == 'colon_lung':
            result = classes_colon_lung[predicted_class_index]

        # Save prediction history to the database
        history_entry = PredictionHistory(
            user_id=user_id,  # Use user_id to link to the User model
            prediction=result
        )

        db.session.add(history_entry)
        db.session.commit()

        return render_template('results.html', model=model_name, result=result)

    return 'Invalid model selected', 400


@app1.route('/results')
def results():
    model = request.args.get('model')
    result = request.args.get('result')
    return f"{model.capitalize()} Model Prediction: {result}"

# Register the Blueprint with the Flask app
app.register_blueprint(app1)

