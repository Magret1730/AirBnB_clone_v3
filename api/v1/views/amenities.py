#!/usr/bin/python3
"""
State view
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity
from models.state import State
from models.city import City


@app_views.route('/amenities', methods=['GET', 'POST'])
def get_amenity():
    """
        amenities route all
    """
    if request.method == 'GET':
        all_amenity = storage.all(Amenity)
        all_amenity = [obj.to_dict() for obj in all_amenity.values()]
        return jsonify(all_amenity)

    if request.method == 'POST':
        try:
            req_json = request.get_json()
        except Exception as e:
            return abort(400, 'Missing name')
        # req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get('name') is None:
            abort(400, 'Missing name')
        new_object = Amenity(**req_json)
        new_object.save()
        return make_response(jsonify(new_object.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def get_amenity_by_id(amenity_id=None):
    """
        amenities route by id
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')

        for key, value in req_json.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)

        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
