#!/usr/bin/python3
"""handle request for state views"""
from flask import jsonify, abort, request
from api.v1.views import api_views
from models.state import State
import models


@app_views.route('/states', strict_slashes=False)
def state():
    """GetS the states from the database"""
    data = []
    storage = models.storage
    states = storage.all(State)
    for state in states:
        state = state.to_dict()
        data.append(state)
    return jsonify(data)


@app_views.route('/states/<state_id>', strict_slashes=False)
def state(state_id):
    """GetS a state from the database"""
    storage = models.storage
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state = state.to_dict()
    return jsonify(state)


@app_views.route('/states/<state_id>', strict_slashes=False, 
                 methods=['DELETE'])
def state(state_id):
    """delete a state from the database, else raise not found error"""
    storage = models.storage
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    return jsonify({})


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def state():
    """adds a state to the database"""
    storage = models.storage
    state = request.get_json(silent=True)
    if state is None:
        return 'Not a JSON', 400
    if state.get('name') is None:
        return 'Missing name', 400
    storage.new(state)
    storage.save()
    return state, 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def state(state_id):
    """modifies a state in the database"""
    storage = models.storage
    state = storage.get(State, state_id)
    if state is None:
        return 'Not a JSON', 400
    state = request.get_json(silent=True)
    if state.get('name') is None:
        return 'Missing name', 400
    storage.new(state)
    storage.save()
    return state, 201
