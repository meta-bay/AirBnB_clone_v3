#!/usr/bin/python3
"""This is a city module"""

from flask import Flask, jsonify, request, abort
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state:
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.content_type != 'application/json':
        abort(400, "Not a JSON")
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    data = request.get_json()
    data['state_id'] = state_id
    new_city = City(**data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.content_type != 'application/json':
        abort(400, "Not a JSON")
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
