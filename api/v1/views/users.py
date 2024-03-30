#!/usr/bin/python3
"""
Users class
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'])
def get_user():
    """
        user route all
    """
    if request.method == 'GET':
        all_user = storage.all(User)
        all_user = [obj.to_dict() for obj in all_user.values()]
        return jsonify(all_user)

    if request.method == 'POST':
        try:
            req_json = request.get_json()
        except Exception as e:
            return abort(400, 'Missing name')
        # req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get('email') is None:
            abort(400, 'Missing email')
        if req_json.get('password') is None:
            abort(400, 'Missing password')
        new_obj = User(**req_json)
        new_obj.save()
        return make_response(jsonify(new_obj.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def get_user_by_id(user_id=None):
    """
        user route by id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404, 'Not a JSON')

    if request.method == 'GET':
        return jsonify(user.to_dict())

    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')

        for key, value in req_json.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(user, key, value)

        storage.save()
        return make_response(jsonify(user.to_dict()), 200)
