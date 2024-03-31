#!/usr/bin/python3
'''
    Status of your API
'''
from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)


app.register_blueprint(app_views)


if __name__ == "__main__":
    the_host = getenv('HBNB_API_HOST', '0.0.0.0')
    the_port = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=the_host, port=the_port, threaded=True)
