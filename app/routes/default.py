from app import app
from flask import render_template, redirect, url_for
from flask_login import login_required

# This is for rendering the home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/alumnimap')
@login_required
def alimnimap():
    return render_template("alumnimap.html")