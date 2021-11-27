from flask import Flask, render_template, request, redirect, url_for, send_from_directory, current_app, make_response
from werkzeug.utils import secure_filename
import os
from MOM_App import predictMOM

# CONSTANT VARIABLES
UPLOAD_FOLDER = 'files\\uploaded'
ALLOWED_EXTENSIONS = set(['wav'])

# GLOBAL VARIABLES
global filename
global fileLocList
fileLocList = []


# APP CONFIG
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
	return render_template('index.html')

def allowed_file(filename):
	# Build the filename + extension after checking if allowed
	# Note: \ == explicit line continuation
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET','POST'])
def upload():
	if request.method == 'POST':
		file = request.files['file']
		enableProcessBtn = False
		# check if the post request has the file part
		if 'file' not in request.files or file.filename == '':
			print("redirected")
			return redirect(url_for('home'))

		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			print("saved file")
			fileLoc = "{}\{}".format(app.config['UPLOAD_FOLDER'],filename)
			print(fileLoc)
			fileLocList.append(fileLoc)
			enableProcessBtn = True
		return render_template('index.html',enableProcessBtn=enableProcessBtn)
	else:
		return redirect(url_for('home'))

@app.route('/processMOM', methods=['GET'])
def processMOM():
	if request.method == 'GET':
		fileLoc = fileLocList.pop()
		resultSummaryText,resultSentimentText = predictMOM(fileLoc)
		print("resultSentimentText",resultSentimentText)
		print("resultSummaryText", resultSummaryText)
		return render_template('index.html',resultSentimentText=resultSentimentText,resultSummaryText=resultSummaryText)
	else:
		return redirect(url_for('home'))

if __name__ == '__main__':
   app.run()