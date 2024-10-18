import os
import logging
from flask import Flask
from app import app1 as prediction_blueprint  # Import the prediction blueprint
from FaceRecognitionModel import app2 as auth_blueprint  # Import the authentication blueprint
from config import Config  # Import your config settings
from models import db  # Import db from models.py
from models import PredictionHistory


from flask_migrate import Migrate
 # Ensure you import your db instance

app = Flask(__name__)
app.config.from_object(Config)

migrate = Migrate(app, db)

# Configure database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///predictions.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

# Initialize SQLAlchemy with the app
db.init_app(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Register blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(prediction_blueprint)


app.secret_key = 'your_secret_key'

# Ensure upload directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all database tables
    app.run(debug=True, port=5000)
