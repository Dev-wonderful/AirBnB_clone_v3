#!/usr/bin/python3
"""handle request for place views"""
from flask import jsonify, abort, request
from api.v1.views import api_views
from models.place import Place
from models.city import City
from models.user import User
import models


@api_views.route('/places', strict_slashes=False)
def get_place():
    """GetS the places from the database"""
    data = []
    storage = models.storage
    places = storage.all(Place).values()
    # loop through each place to convert to dict
    for place in places:
        place = place.to_dict()
        data.append(place)
    return jsonify(data)


@api_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places_by_city(city_id):
    """Gets the places in a city from the database"""
    storage = models.storage
    data = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for place in city.places:
        place = place.to_dict()
        data.append(place)
    return jsonify(data)


@api_views.route('/places/<place_id>', strict_slashes=False)
def get_place_by_id(place_id):
    """GetS a place from the database"""
    storage = models.storage
    # check for presence and return, else throw error
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place = place.to_dict()
    return jsonify(place)


@api_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """delete a place from the database, else raise not found error"""
    storage = models.storage
    # check for presence and return, else throw error
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@api_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def add_place(city_id):
    """adds a place to the database"""
    storage = models.storage
    # get json data or silently return None if not a json type
    place = request.get_json(silent=True)
    if place is None:
        return 'Not a JSON', 400
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    # check for presence of required param
    if place.get('user_id') is None:
        return 'Missing user_id', 400
    elif place.get('name') is None:
        return 'Missing name', 400
    user_id = place.get('user_id')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    place['city_id'] = city_id
    new_instance = Place(**place)
    new_instance.save()
    return new_instance.to_dict(), 201


@api_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def modify_place(place_id):
    """modifies a place in the database"""
    storage = models.storage
    # check for presence and return, else throw error
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    # get json data or silently return None if not a json type
    place_update = request.get_json(silent=True)
    if place_update is None:
        return 'Not a JSON', 400
    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in place_update.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return place.to_dict()
