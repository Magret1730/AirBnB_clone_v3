#!/usr/bin/python3
"""
State view
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state(state_id=None):
    """Get state object"""
    state_by_id = storage.get(State, state_id)
    if state_by_id is None:
        abort(404, 'Not found')
    cities = [city.to_dict() for city in state_by_id.cities]
    return jsonify(cities)


@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_cities(city_id=None):
    """Get state object based on ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404, 'Not found')
    return jsonify(city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def Del_city(city_id=None):
    """Get state object based on ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404, 'Not found')
    else:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_cities_by_state(state_id=None):
    """Get state object"""
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    if req_json.get("name") is None:
        abort(400, 'Missing name')
    req_json['state_id'] = state_id
    new_city = City(**req_json)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id=None):
    """Get state object based on ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404, 'Not found')
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')

    for key, value in req_json.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    storage.save()

    return make_response(jsonify(city.to_dict()), 200)
