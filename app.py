from flask import Flask
from config import Configuration
from serverlogs.blueprint import server_logs

app = Flask(__name__)
app.config.from_object(Configuration)

app.register_blueprint(server_logs, url_prefix='/serverlogs')
