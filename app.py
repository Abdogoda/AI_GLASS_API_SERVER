# ---------------------------------------
# Import Libraries ----------------------
# ---------------------------------------
import os
import shutil
import numpy as np
from waitress import serve
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, jsonify
from finder_and_depth_estimation import find, test_find
from detection_function import *
from describe_function import generate_caption_from_image, test_describe
from ocr_function import ocr_image_to_text, test_ocr

# ---------------------------------------
# Define a Flask app --------------------
# ---------------------------------------
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"

# ---------------------------------------
# Test The Program Functions ------------
# ---------------------------------------
print("Testing the Description Mode ............")
test_describe()
print("Done ✔️")
print("Testing the Ocr Text Mode ............")
test_ocr()
print("Done ✔️")
print("Testing the Finder Mode ............")
test_find()
print("Done ✔️")
print("Testing the Detection Mode ............")
test_detection()
print("Done ✔️")
print("---------------------------------------------------")
print("The Program Is Ready ✔️ ---------------------------")
print("---------------------------------------------------")


# ---------------------------------------
# Helper functions ----------------------
# ---------------------------------------
def save_file(file):
    # create folder with name of the day
    today_date = datetime.now().strftime('%Y-%m-%d')
    today_folder_path = os.path.join(UPLOAD_FOLDER, today_date)
    if not os.path.exists(today_folder_path):
        os.makedirs(today_folder_path)
    
    # Remove folders with names other than today's date
    for folder in os.listdir(UPLOAD_FOLDER):
        folder_path = os.path.join(UPLOAD_FOLDER, folder)
        if os.path.isdir(folder_path) and folder != today_date:
            shutil.rmtree(folder_path)

    # Save the image with the current datetime
    filename = secure_filename(file.filename)
    filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S_') + filename
    file_path = os.path.join(today_folder_path, filename)
    file.save(file_path)
    return today_folder_path+'/'+filename



# ---------------------------------------
# The Main Route For Web ----------------
# ---------------------------------------
@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


# ---------------------------------------
# The Detection Route -------------------
# ---------------------------------------
@app.route('/detect', methods=['POST'])
def detect():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify([{
                'result': 'Something Went Wrong!',
                'mode' : 'object'
            }])
        
        print("Processing ............")

        # Get the file from post request
        f = request.files['file']

        # Call save image function 
        file_path = save_file(f)

        # Make prediction
        result = None
        selected_option = request.form.get('select_mode')
        if(selected_option == "currency"):
            result = (file_path, "currency")
        elif(selected_option == "describe"):
            result = generate_caption_from_image(file_path)
        elif(selected_option == "text"):
            result = ocr_image_to_text(file_path)
        elif(selected_option == "find"):
            object_to_be_found = request.form.get('object_to_be_found')
            result = find(file_path, object_to_be_found)
        else:
            result = image_detection(file_path, "object")

        print("Response Sent Successfully\n")
        return jsonify([
            {
                'result' : result,
                'mode' : selected_option
            }
        ])
    return None



# ---------------------------------------
# Run The App ---------------------------
# ---------------------------------------
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5001)

