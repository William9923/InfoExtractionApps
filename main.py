from flask import Flask,redirect,url_for, render_template, request
from werkzeug.utils import secure_filename 
app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def webpage():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(port=3000,debug=True)

