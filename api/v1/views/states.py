#!/usr/bin/python3
"""handle request for state views"""
from flask import jsonify, abort, request
from api.v1.views import api_views
from models.state import State
import models


@api_views.route('/states', strict_slashes=False)
def get_state():
    """GetS the states from the database"""
    data = []
    storage = models.storage
    states = storage.all(State).values()
    # loop through each state to convert to dict
    for state in states:
        print('get states')
        print(state)
        state = state.to_dict()
        data.append(state)
    return jsonify(data)


@api_views.route('/states/<state_id>', strict_slashes=False)
def get_state_by_id(state_id):
    """GetS a state from the database"""
    storage = models.storage
    # check for presence and return, else throw error
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state = state.to_dict()
    return jsonify(state)


@api_views.route('/states/<state_id>', strict_slashes=False, 
                 methods=['DELETE'])
def delete_state(state_id):
    """delete a state from the database, else raise not found error"""
    storage = models.storage
    # check for presence and return, else throw error
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    return jsonify({})


@api_views.route('/states', strict_slashes=False, methods=['POST'])
def add_state():
    """adds a state to the database"""
    storage = models.storage
    # get json data or silently return None if not a json type
    state = request.get_json(silent=True)
    if state is None:
        return 'Not a JSON', 400
    # check for presence of required param
    if state.get('name') is None:
        return 'Missing name', 400
    storage.new(state)
    storage.save()
    return state, 201


@api_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def modify_state(state_id):
    """modifies a state in the database"""
    storage = models.storage
    # check for presence and return, else throw error
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    # get json data or silently return None if not a json type
    state_update = request.get_json(silent=True)
    if state_update is None:
        return 'Not a JSON', 400
    # check for presence of required param
    if state_update.get('name') is None:
        return 'Missing name', 400
    state.name = state_update.get('name')
    storage.save()
    return state, 201
