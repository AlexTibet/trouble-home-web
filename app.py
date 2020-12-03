from flask import Flask
from config import Configuration


app = Flask(__name__)
app.config.from_object(Configuration)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
