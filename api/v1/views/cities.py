#!/usr/bin/python3
"""handle request for city views"""
from flask import jsonify, abort, request
from api.v1.views import api_views
from models.city import City
import models


@api_views.route('/cities', strict_slashes=False)
def get_cities():
    """GetS the cities from the database"""
    data = []
    storage = models.storage
    cities = storage.all(City).values()
    # loop through each city to convert to dict
    for city in cities:
        city = city.to_dict()
        data.append(city)
    return jsonify(data)


@api_views.route('/cities/<city_id>', strict_slashes=False)
def get_city_by_id(city_id):
    """GetS a city from the database"""
    storage = models.storage
    # check for presence and return, else throw error
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city = city.to_dict()
    return jsonify(city)


@api_views.route('/cities/<city_id>', strict_slashes=False, 
                 methods=['DELETE'])
def delete_city(city_id):
    """delete a city from the database, else raise not found error"""
    storage = models.storage
    # check for presence and return, else throw error
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    return jsonify({})


@api_views.route('/cities', strict_slashes=False, methods=['POST'])
def add_city():
    """adds a city to the database"""
    storage = models.storage
    # get json data or silently return None if not a json type
    city = request.get_json(silent=True)
    if city is None:
        return 'Not a JSON', 400
    # check for presence of required param
    if city.get('name') is None:
        return 'Missing name', 400
    storage.new(city)
    storage.save()
    return city, 201


@api_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def modify_city(city_id):
    """modifies a city in the database"""
    storage = models.storage
    # check for presence and return, else throw error
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    # get json data or silently return None if not a json type
    city_update = request.get_json(silent=True)
    if city_update is None:
        return 'Not a JSON', 400
    # check for presence of required param
    if city_update.get('name') is None:
        return 'Missing name', 400
    city.name = city_update.get('name')
    storage.save()
    return city, 201
