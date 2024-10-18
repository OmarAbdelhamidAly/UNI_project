# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///site.db')  # Change to your database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
