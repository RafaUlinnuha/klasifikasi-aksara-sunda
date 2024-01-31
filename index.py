from flask import Flask, render_template, request, redirect, flash, url_for
import main
import urllib.request
from app import app
from werkzeug.utils import secure_filename
from main import getPrediction
import os

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aksara-swara')
def aksara_swara():
    return render_template('swara.html')

@app.route('/aksara-ngalagena')
def aksara_ngalagena():
    return render_template('ngalagena.html')

@app.route('/aksara-khusus')
def aksara_khusus():
    return render_template('khusus.html')

@app.route('/', methods=['POST'])
def submit_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            getPrediction(filename)
            label, acc = getPrediction(filename)
            flash(label, 'class')
            flash(acc, 'accuracy')
            flash(filename, 'filename')
            return redirect('/')
        
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)