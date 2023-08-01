#!/usr/bin/python3
"""api route created here"""
from api.v1.views import api_views
from flask import jsonify
import models
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@api_views.route('/status', strict_slashes=False)
def status():
    """return the status of the api"""
    data = {
        "status": "OK"
    }
    return jsonify(data)


@api_views.route('/stats', strict_slashes=False)
def stats():
    """return the statistics of all objects grouped by class"""
    storage = models.storage
    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }
    data = {}
    for clas_str, clas in classes.items():
        count = storage.count(clas)
        data[clas_str] = count
    return jsonify(data)
