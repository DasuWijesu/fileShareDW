from flask import Flask, request, redirect, url_for, render_template, send_from_directory, flash
import os
import logging

logging.basicConfig(level=logging.DEBUG)  # Configure logging level as needed

app = Flask(__name__)

# Set the folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return files

@app.route('/')
def index():
    files = list_files()
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash('File {} deleted.'.format(filename), 'success')
    else:
        flash('File {} not found.'.format(filename), 'error')
    return redirect(url_for('index'))

@app.errorhandler(500)
def server_error(e):
    logging.error('An internal server error occurred: %s', e)
    return 'Internal Server Error', 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
