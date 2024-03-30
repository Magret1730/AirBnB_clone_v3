#!/usr/bin/python3
"""
State view
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def get_state():
    """Get state object"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_id(state_id):
    """Get state object based on ID"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        return abort(404, 'Not found')


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete state object based on ID"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404, 'Not found')


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates new state"""
    try:
        data = request.get_json()
    except Exception as e:
        return abort(400, 'Missing name')
    # data = request.get_json()
    if data is None:
        return abort(400, 'Not a JSON')
    if 'name' not in data:
        return abort(400, 'Missing name')

    new_state = State(**data)
    new_state.save()

    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a State"""
    state = storage.get(State, state_id)
    if not state:
        return abort(404, 'Not found')

    data = request.get_json()
    if data is None:
        return abort(400, 'Not a JSON')

    # Update state object with new data
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    state.save()
    return make_response(jsonify(state.to_dict()), 200)
