#!/usr/bin/python3
"""api route created here"""
from api.v1.views import api_views
from flask import jsonify


@api_views.route('/status', strict_slashes=False)
def status():
    """return the status of the api"""
    data = {
        "status": "OK"
    }
    return jsonify(data)
