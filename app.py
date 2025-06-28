import os
from flask import Flask, request, send_from_directory, render_template
from PIL import Image

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESIZED_FOLDER = 'static/resized'

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESIZED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    if file.filename == '':
        return "No selected file"

    # Save original image
    original_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(original_path)

    # Resize image
    with Image.open(original_path) as img:
        resized = img.resize((300, 200))
        resized_filename = f"resized_{file.filename}"
        resized_path = os.path.join(RESIZED_FOLDER, resized_filename)
        resized.save(resized_path)

    return f'''
        <p>Image uploaded and resized!</p>
        <a href="/download/{resized_filename}">Download Resized Image</a>
    '''

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(RESIZED_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
