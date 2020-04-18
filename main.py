import os
from pprint import pprint
from flask import Flask, redirect, url_for, render_template, request, flash
from util import *

from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def webpage():
	keyword = request.form.get('keyword')
	algo = request.form.get('algo')
	files = request.files.getlist("files[]")
	if request.method == 'POST' and validate(keyword, algo, files):
		list_of_files = create_file(files)
		result = create_answer(algo, keyword, list_of_files)
		return render_template('index.html', keyword=keyword.strip(), results=result)
	return render_template('index.html')

if __name__ == '__main__':
	app.run(port=3000, debug=True)
