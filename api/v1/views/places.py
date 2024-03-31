#!/usr/bin/python3
"""
Place class
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id=None):
    """Get all place object"""
    city_by_id = storage.get(City, city_id)
    if city_by_id is None:
        abort(404)
    places = [place.to_dict() for place in city_by_id.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_places(place_id=None):
    """Get place object based on ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def Del_place(place_id=None):
    """Delete place object based on ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_cities_by_places(city_id=None):
    """Create a new Place associated with a City"""
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    if "user_id" not in req_json:
        abort(400, 'Missing user_id')
    user_id = req_json["user_id"]
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if "name" not in req_json:
        abort(400, 'Missing name')

    req_json['city_id'] = city_id
    new_place = Place(**req_json)
    new_place.save()

    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Update a Place object by ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')

    # Ignore keys: id, user_id, city_id, created_at, updated_at
    keys_to_ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key in keys_to_ignore:
        req_json.pop(key, None)

    # Update Place object with new data
    for key, value in req_json.items():
        setattr(place, key, value)

    storage.save()

    return make_response(jsonify(place.to_dict()), 200)
