#!/usr/bin/python3
"""handle request for city views"""
from flask import jsonify, abort, request
from api.v1.views import api_views
from models.city import City
from models.state import State
import models


@api_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities_by_state(state_id):
    """Gets the cities from a state in the database"""
    storage = models.storage
    data = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for city in state.cities:
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


@api_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def add_city(state_id):
    """adds a city to the database"""
    storage = models.storage
    # get json data or silently return None if not a json type
    city = request.get_json(silent=True)
    if city is None:
        return 'Not a JSON', 400
    # check for existence of state and presence of required param
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if city.get('name') is None:
        return 'Missing name', 400
    city['state_id'] = state_id
    new_instance = City(**city)
    return new_instance.to_dict(), 201


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
    return city.to_dict()
