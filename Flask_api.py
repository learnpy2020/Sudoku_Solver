#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 17:22:24 2020

@author: pushkara
"""
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
import os
from image_processing import grid_to_metrix
import algo 


app = Flask(__name__)

def detect_solve(path):
    grid = grid_to_metrix(path)
    if algo.solve(grid) :
        print('#'*34+'\nSolved ans is : ')
        algo.print_board(grid)
        return 'Solved'
    else:
        print("Detection Error!")
        return 'Detection Error!'
    

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        grid = detect_solve(file_path)
        
        result = str(grid)               # Convert to string
        return result
    return None



if __name__ == "__main__":
    app.run(debug=False)