from flask import Blueprint, request, jsonify, session
from pymysql.err import IntegrityError

from app.services.auth_service import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    verify_user,
)

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    existing_user = get_user_by_email(email)
    if existing_user:
        return jsonify({"error": "Email already registered"}), 409

    try:
        user_id = create_user(email, password)
    except IntegrityError:
        return jsonify({"error": "Email already registered"}), 409

    session["user_id"] = user_id

    return jsonify({
        "message": "Registration successful",
        "user": {
            "id": user_id,
            "email": email
        }
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = verify_user(email, password)
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    session["user_id"] = user["id"]

    return jsonify({
        "message": "Login successful",
        "user": user
    }), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Logout successful"}), 200


@auth_bp.route("/me", methods=["GET"])
def me():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"authenticated": False}), 200

    user = get_user_by_id(user_id)
    if not user:
        session.pop("user_id", None)
        return jsonify({"authenticated": False}), 200

    return jsonify({
        "authenticated": True,
        "user": user
    }), 200