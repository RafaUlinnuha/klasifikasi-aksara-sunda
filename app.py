from flask import Flask

# Specify the folder where uploaded files will be stored
UPLOAD_FOLDER = '../web/uploads'

# Create a Flask web application instance
app = Flask(__name__)

# Set a secret key for the application (used for session management and security)
app.secret_key = "secret key"

# Configure the application to use the specified UPLOAD_FOLDER for file uploads
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER