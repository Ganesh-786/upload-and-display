from flask import Flask, render_template, request, redirect, url_for,send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_DIRECTORY']='uploads/'
UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return render_template('uploaded_file.html', filename=filename)

# @app.route('/serve-image/<filename>',methods=["GET"])
# def serve_image(filename):
#     return send_from_directory(app.config['UPLOAD_DIRECTORY'],filename)

if __name__ == '__main__':
    app.run(debug=True)
