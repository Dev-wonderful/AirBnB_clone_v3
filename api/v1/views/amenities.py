#!/usr/bin/python3
"""handle request for amenity views"""
from flask import jsonify, abort, request
from api.v1.views import api_views
from models.amenity import Amenity
import models


@api_views.route('/amenities', strict_slashes=False)
def get_amenities():
    """GetS the amenities from the database"""
    data = []
    storage = models.storage
    amenities = storage.all(Amenity).values()
    # loop through each amenity to convert to dict
    for amenity in amenities:
        amenity = amenity.to_dict()
        data.append(amenity)
    return jsonify(data)


@api_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """GetS a amenity from the database"""
    storage = models.storage
    # check for presence and return, else throw error
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity = amenity.to_dict()
    return jsonify(amenity)


@api_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """delete a amenity from the database, else raise not found error"""
    storage = models.storage
    # check for presence and return, else throw error
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({})


@api_views.route('/amenities', strict_slashes=False, methods=['POST'])
def add_amenity():
    """adds a amenity to the database"""
    # storage = models.storage
    # get json data or silently return None if not a json type
    amenity = request.get_json(silent=True)
    if amenity is None:
        return 'Not a JSON', 400
    # check for presence of required param
    if amenity.get('name') is None:
        return 'Missing name', 400
    new_instance = Amenity(**amenity)
    new_instance.save()
    return new_instance.to_dict(), 201


@api_views.route('/amenities/<amenity_id>', strict_slashes=False, 
                 methods=['PUT'])
def modify_amenity(amenity_id):
    """modifies a amenity in the database"""
    storage = models.storage
    # check for presence and return, else throw error
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    # get json data or silently return None if not a json type
    amenity_update = request.get_json(silent=True)
    if amenity_update is None:
        return 'Not a JSON', 400
    # check for presence of required param
    if amenity_update.get('name') is None:
        return 'Missing name', 400
    amenity.name = amenity_update.get('name')
    storage.save()
    return amenity.to_dict()
