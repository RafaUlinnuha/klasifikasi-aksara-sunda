from flask import Flask
import os

# Set up the upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

# Create a Flask web application instance
app = Flask(__name__)

# Set a secret key for the application (used for session management and security)
app.secret_key = "secret key"

# Configure the application to use the specified UPLOAD_FOLDER for file uploads
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
