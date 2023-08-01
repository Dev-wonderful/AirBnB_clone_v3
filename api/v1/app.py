#!/usr/bin/python3
"""Api for our app"""
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import api_views

app = Flask(__name__)
app.register_blueprint(api_views)


@app.errorhandler(404)
def not_found(error):
    """handles not found errors"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def end_session(error=None):
    """close the database after a request session"""
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')
    app.run(host=host, port=port, threaded=True)
