#!/usr/bin/python3
"""handle request for review views"""
from flask import jsonify, abort, request
from api.v1.views import api_views
from models.review import Review
from models.place import Place
from models.user import User
import models


@api_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_reviews_by_place(place_id):
    """Gets the reviews in a place from the database"""
    storage = models.storage
    data = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for review in place.reviews:
        review = review.to_dict()
        data.append(review)
    return jsonify(data)


@api_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review_by_id(review_id):
    """GetS a review from the database"""
    storage = models.storage
    # check for presence and return, else throw error
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review = review.to_dict()
    return jsonify(review)


@api_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """delete a review from the database, else raise not found error"""
    storage = models.storage
    # check for presence and return, else throw error
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@api_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def add_review(place_id):
    """adds a review to the database"""
    storage = models.storage
    # get json data or silently return None if not a json type
    review = request.get_json(silent=True)
    if review is None:
        return 'Not a JSON', 400

    # check if the place exists
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    # check for existence of required param
    if review.get('user_id') is None:
        return 'Missing user_id', 400
    if review.get('text') is None:
        return 'Missing text', 400
    user_id = place.get('user_id')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    review['place_id'] = place_id
    new_instance = Review(**review)
    new_instance.save()
    return new_instance.to_dict(), 201


@api_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def modify_review(review_id):
    """modifies a review in the database"""
    storage = models.storage
    # check for presence and return, else throw error
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    # get json data or silently return None if not a json type
    review_update = request.get_json(silent=True)
    if review_update is None:
        return 'Not a JSON', 400
    # check for presence of required param
    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in review_update.items():
        if key not in ignore:
            setattr(review, key, value)
    storage.save()
    return review.to_dict()
