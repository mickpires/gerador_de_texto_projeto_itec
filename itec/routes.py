from flask import render_template, url_for, redirect
from itec import app

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')