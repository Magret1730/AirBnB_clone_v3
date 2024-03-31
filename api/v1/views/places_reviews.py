#!/usr/bin/python3
"""
State view
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews_by_places(place_id=None):
    """Get all review objects"""
    place_by_id = storage.get(Place, place_id)
    if place_by_id is None:
        abort(404)
    reviews = [review.to_dict() for review in place_by_id.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_reviews(review_id=None):
    """Get review object based on ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/eviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    """Deletes review object based on ID"""
    review = storage.get(Review, review_id)
    if not Review:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_reviews_by_places(place_id=None):
    """Creates new review object associated by Places"""
    place = storage.get(Place, place_id)
    if not Place:
        abort(404)

    req_json = request.get_json()
    if not req_json:
        abort(400, 'Not a JSON')

    required_keys = ['user_id', 'text']
    for key in required_keys:
        if key not in req_json:
            abort(400, 'Missing {}'.format(key))

    user = storage.get(User, req_json['user_id'])
    if not User:
        abort(404)

    review = Review(place_id=place_id, **req_json)
    review.save()

    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a Review object by ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    req_json = request.get_json()
    if not req_json:
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in req_json.items():
        if key not in ignore_keys:
            setattr(review, key, value)

    review.save()

    return make_response(jsonify(review.to_dict()), 200)
