from flask import Blueprint, jsonify, session
from pymysql.err import IntegrityError

from app.services.favorite_service import (
    get_user_favorites,
    add_favorite,
    remove_favorite,
    is_favorite,
)
from app.services.queries import get_station_latest

favorites_bp = Blueprint("favorites", __name__, url_prefix="/api/favorites")


def require_login():
    user_id = session.get("user_id")
    if not user_id:
        return None, (jsonify({"error": "Authentication required"}), 401)
    return user_id, None


@favorites_bp.route("", methods=["GET"])
def list_favorites():
    user_id, error_response = require_login()
    if error_response:
        return error_response

    favorites = get_user_favorites(user_id)
    return jsonify(favorites), 200


@favorites_bp.route("/<int:station_number>", methods=["POST"])
def create_favorite(station_number):
    user_id, error_response = require_login()
    if error_response:
        return error_response

    station = get_station_latest(station_number)
    if not station:
        return jsonify({"error": "Station not found"}), 404

    try:
        add_favorite(user_id, station_number)
    except IntegrityError:
        return jsonify({"message": "Station already in favorites"}), 200

    return jsonify({"message": "Favorite added"}), 201


@favorites_bp.route("/<int:station_number>", methods=["DELETE"])
def delete_favorite(station_number):
    user_id, error_response = require_login()
    if error_response:
        return error_response

    removed = remove_favorite(user_id, station_number)
    if not removed:
        return jsonify({"error": "Favorite not found"}), 404

    return jsonify({"message": "Favorite removed"}), 200


@favorites_bp.route("/<int:station_number>/status", methods=["GET"])
def favorite_status(station_number):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"is_favorite": False, "authenticated": False}), 200

    return jsonify({
        "authenticated": True,
        "is_favorite": is_favorite(user_id, station_number)
    }), 200