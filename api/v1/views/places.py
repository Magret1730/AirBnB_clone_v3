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
from models.amenity import Amenity


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


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """
        places search
    """
    places_all = [place for place in storage.all(Place).values()]

    # check the request content
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')

    # get the states and the cities to look from for places
    states_asked = req_json.get('states')
    if states_asked and len(states_asked) > 0:
        all_cities = storage.all(City)
        cities_by_state = set([city.id for city in all_cities.values()
                               if city.state_id in states_asked])
    else:
        cities_by_state = set()

    # get the cities
    cities_asked = req_json.get('cities')
    if cities_asked and len(cities_asked) > 0:
        cities_asked = set([
            c_id for c_id in cities_asked if storage.get(City, c_id)])
        cities_by_state = cities_by_state.union(cities_asked)

    # get the amenities
    amenity_asked = req_json.get('amenities')
    if len(cities_by_state) > 0:
        places_all = (
            [pla for pla in places_all if pla.city_id in cities_by_state]
            )
    elif amenity_asked is None or len(amenities) == 0:
        return make_response(
            jsonify([place.to_dict() for place in places_all])
            )

    # place amenity
    places_amenities = []
    if amenity_asked and len(amenity_asked) > 0:
        amenity_asked = set(
            [a_id for a_id in amenity_asked if storage.get(Amenity, a_id)]
            )
        for pla in places_all:
            place_amentiy = None
            if STORAGE_TYPE == 'db' and pla.amenities:
                place_amentiy = [a.id for a in pla.amenities]
            elif len(pla.amenities) > 0:
                place_amentiy = pla.amenities
            if place_amentiy and (
                   all([pl in place_amentiy for pl in amenities])
                   ):
                places_amenities.append(pla)
    else:
        places_amenities = places_all
    return make_response(
        jsonify([place.to_dict() for place in places_amenities])
        )
