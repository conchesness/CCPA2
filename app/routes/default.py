from app import app
from flask import render_template, redirect, url_for

# This is for rendering the home page
@app.route('/')
def index():
    return redirect(url_for('wordcloud'))