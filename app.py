from flask import Flask, render_template, send_from_directory, abort
import os

app = Flask(__name__)

# Set the folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to list files in the uploads folder
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return files

@app.route('/')
def index():
    files = list_files()
    return render_template('index.html', files=files)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/metadata/<filename>')
def view_metadata(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        abort(404)
    
    metadata = {
        'filename': filename,
        'size': os.path.getsize(filepath)
    }
    return render_template('metadata.html', metadata=metadata)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
