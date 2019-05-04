from flask import Flask,render_template,request
from werkzeug import secure_filename
from Colorize import colorize
from flask import send_file
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
 return render_template('index.html')
@app.route('/output',methods=['GET','POST'])
def output():
    if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      out_name = colorize(f.filename)
      return send_file(out_name, as_attachment=True)
      #return 'file uploaded successfully'

if __name__ == '__main__':
    app.run(debug=True)
