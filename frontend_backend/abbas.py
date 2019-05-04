from flask import Flask,render_template,request
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
@app.route('/output',methods=['GET','POST'])
def output():
    if request.method == 'POST':
      file_name = './input.jpg'
      print('flag')
      print(request.form)
      print(request.files['file'])
      url = request.form.get('url')
      f = request.files.get('file')
      if url is not '':
        image = urllib.request.URLopener()
        image.retrieve(url, file_name)
      elif f.filename is not '':
        file_name = f.filename
        f.save(secure_filename(file_name))
      else:
        return ('', 204)
      out_name = colorize(file_name)
      os.remove(file_name)
      return send_file(out_name, as_attachment=True)
      #return 'file uploaded successfully'

if __name__ == '__main__':
    app.run(debug=True)
