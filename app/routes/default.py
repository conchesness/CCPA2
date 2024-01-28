from app import app
from flask import render_template, redirect, url_for

# This is for rendering the home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/alumnimaptest')
def alimnimaptest():
    return render_template("alumnimap/index.html")

@app.route('/alumnimap')
def alimnimap():
    return render_template("alumnimap.html")