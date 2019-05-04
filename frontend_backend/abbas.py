from flask import Flask, render_template, request, jsonify
from werkzeug import secure_filename
from Colorize import colorize
from flask import send_file
import urllib
import os

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/output', methods=['POST'])
def output():
    file_name = './static/input.jpg'
    out_name = './static/out.jpg'
    url = request.form.get('url')
    f = request.files.get('file')
    if url:
        image = urllib.request.URLopener()
        image.retrieve(url, file_name)
    elif f:
        f.save(file_name)
    else:
        return jsonify({'error': 'Please Choose File OR Paste URL!'})
    colorize(file_name, out_name)
    #os.remove(file_name)
    return jsonify({'input_path':file_name, 'img_path': out_name})


if __name__ == '__main__':
    app.run(debug=True)

# action='http://127.0.0.1:5000/output' method="POST" enctype = "multipart/form-data">
