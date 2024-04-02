#!/usr/bin/python3
"""This is the places module"""

from flask import Flask, jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from models.amenity import Amenity
from models.state import State


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city:
        places = [place.to_dict() for place in city.places]
        return jsonify(places)
    else:
        abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.content_type != 'application/json':
        abort(400, "Not a JSON")
    if not request.json:
        abort(400, "Not a JSON")
    if 'user_id' not in request.json:
        abort(400, "Missing user_id")
    if 'name' not in request.json:
        abort(400, "Missing name")
    user_id = request.json['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    data['city_id'] = city_id
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.content_type != 'application/json':
        abort(400, "Not a JSON")
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'],  strict_slashes=False)
def places_search():
    """Search for places based on given criteria"""
    # Parse the JSON body of the request
    data = request.get_json()
    if request.content_type != 'application/json':
        abort(400, "Not a JSON")
    if not request.json:
        abort(400, "Not a JSON")
    # data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    # if request.content_type != 'application/json':
    #    abort(400, "Not a JSON")
    # if not request.json:
    #    abort(400, "Not a JSON")

    # Extract the optional keys from the JSON
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    # Retrieve all places if JSON body is empty or all keys are empty
    if not states and not cities and not amenities:
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    # Filter places based on states and cities
    place_ids = set()
    for state_id in states:
        state = storage.get(State, state_id)
        if state:
            for city in state.cities:
                place_ids.update(place.id for place in city.places)
    for city_id in cities:
        city = storage.get(City, city_id)
        if city:
            place_ids.update(place.id for place in city.places)

    # Filter places based on amenities
    if amenities:
        for amenity_id in amenities:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                place_ids.intersection_update(
                    place.id for place in place_ids if amenity
                    in place.amenities)

    # Retrieve the places based on filtered place ids
    places = [storage.get(Place, place_id).to_dict() for place_id in place_ids]
    return jsonify(places)
