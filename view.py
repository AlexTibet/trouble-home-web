from app import app
from flask import render_template


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/serverconfig')
def server_config():
    return render_template('server_config.html')


@app.route('/troublebots')
def trouble_bots():
    return render_template('trouble_bots.html')
