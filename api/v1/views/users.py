#!/usr/bin/python3
"""handle request for user views"""
from flask import jsonify, abort, request
from api.v1.views import api_views
from models.user import User
import models


@api_views.route('/users', strict_slashes=False)
def get_user():
    """GetS the users from the database"""
    data = []
    storage = models.storage
    users = storage.all(User).values()
    # loop through each user to convert to dict
    for user in users:
        user = user.to_dict()
        data.append(user)
    return jsonify(data)


@api_views.route('/users/<user_id>', strict_slashes=False)
def get_user_by_id(user_id):
    """GetS a user from the database"""
    storage = models.storage
    # check for presence and return, else throw error
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user = user.to_dict()
    return jsonify(user)


@api_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """delete a user from the database, else raise not found error"""
    storage = models.storage
    # check for presence and return, else throw error
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@api_views.route('/users', strict_slashes=False, methods=['POST'])
def add_user():
    """adds a user to the database"""
    # storage = models.storage
    # get json data or silently return None if not a json type
    user = request.get_json(silent=True)
    if user is None:
        return 'Not a JSON', 400
    # check for presence of required param
    if user.get('email') is None:
        return 'Missing email', 400
    elif user.get('password') is None:
        return 'Missing password', 400
    new_instance = User(**user)
    new_instance.save()
    return new_instance.to_dict(), 201


@api_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def modify_user(user_id):
    """modifies a user in the database"""
    storage = models.storage
    # check for presence and return, else throw error
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    # get json data or silently return None if not a json type
    user_update = request.get_json(silent=True)
    if user_update is None:
        return 'Not a JSON', 400
    ignore = ['id', 'email', 'created_at', 'updated_at']
    for key, value in user_update.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return user.to_dict()
