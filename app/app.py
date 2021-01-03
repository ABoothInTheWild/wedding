import os
from flask import Flask, render_template, jsonify, request, Response, send_from_directory
import json
import csv
from sqlFactory import SQLFactory
from credentials import *
import pandas as pd
import datetime
import numpy as np

# Create an instance of Flask
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#SQL Factory
sf = SQLFactory()

# Favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

# Route to render html templates
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route('/loginAttempt/', methods=["POST"])
def loginAttempt():
    content = request.json["data"]

    #parse params
    password = content["password"]

    #check login attempt
    success = False
    if (password == PASSWORD):
        success = True

    return(jsonify({"success": success}))

@app.route('/adminLoginAttempt/', methods=["POST"])
def adminLoginAttempt():
    content = request.json["data"]

    #parse params
    login = content["login"]
    password = content["password"]

    #check login attempt
    success = False
    if ((login == ADMIN_USERNAME) & (password == ADMIN_PASSWORD)):
        success = True

    return(jsonify({"success": success}))

@app.route('/saveFormData/', methods=["POST"])
def saveFormData():
    content = request.json["data"]
    formInfo = content["formInfo"]

    success = sf.saveDataToDatabase(formInfo)
    success = {"ok": True}
    return(jsonify({"success": success["ok"]}))

@app.route('/getAllData/', methods=["POST"])
def getAllData():
    content = request.json["data"] #unused
    data = sf.getAllData()
    return(jsonify(json.loads(data.to_json(orient="records"))))

#############################################################
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

#main
if __name__ == "__main__":
    # app.run(debug=False, host="0.0.0.0")
    app.run(debug=True)
