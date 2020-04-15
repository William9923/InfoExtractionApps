from flask import Flask, url_for, render_template, redirect
from flask import request # to get the data from form / any other post request
from werkzeug.utils import secure_filename # for processing with filenames
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])  # routing option in flask
def index():
	return "Hello World"

@app.route('/<name>/', methods=['GET'])
def hello(name):
	return f"Hello {name}"

@app.route('/<int:number>/', methods=['GET'])
def printNumber(number):
	return f"Number to print : {number}"

# Path variable rules : <converter:variable_name>
@app.route('/<float:decimal>', methods=['GET'])
def printDecimal(decimal):
	return f"Decimal to print : {decimal}"


@app.route('/website', methods=['GET'])
def getPage():
	return render_template('index.html', name="William", exercise="Tugas Kecil Stima 4")

@app.route('/login', methods=['POST','GET'])    # Example of handling with request object / via form
def login():
	if request.method == 'POST' :
		username = request.form['uname']
		password = request.form['password']
		file = request.files['samplefile']
		if file is not None:
			filename = secure_filename(file.filename)
			file.save(os.path.join("static",filename))
			with open(os.path.join("static",file.filename)) as f:
				file_content = f.readline()
			print("File Content: ")
			print(file_content)
		print("Username : " + username)
		print("Password : " + password)
		return redirect(url_for('getPage'))
	else :
		print(request.args.get("duar")) # Buat dapetin data dari query string 
		return render_template('form.html')

# Kode di bawah buat ngelakuin testing url:
# with app.test_request_context():
# 		print(url_for('index',duar="Heheheh")) # kalo dia ga jd parameter-> dia jd query string buat kodeny, ho baru tau aku
# 		print(url_for('hello', name="William"))
# 		print(url_for('printNumber', number=10))
		
if __name__=='__main__':
	app.run(port=3000,debug=True)

