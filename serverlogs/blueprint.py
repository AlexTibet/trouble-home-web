from flask import Blueprint, render_template


server_logs = Blueprint('server_logs', __name__, template_folder='templates')


@server_logs.route('/')
def index():
    return render_template('serverlogs/index.html')
