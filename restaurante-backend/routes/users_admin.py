from flask import Blueprint, request, jsonify
from ..utils import admin_required
from .. import db
from ..models import User

bp = Blueprint("users_admin", __name__)

@bp.route("/users", methods=["GET"])
@admin_required
def list_users():
    users = User.query.order_by(User.id.desc()).all()
    return jsonify([{"id": u.id, "email": u.email, "name": u.name, "role": u.role} for u in users]), 200

@bp.route("/users", methods=["POST"])
@admin_required
def create_user():
    data = request.get_json() or {}
    email = data.get("email")
    name = data.get("name")
    password = data.get("password")
    role = data.get("role", "client")

    if not email or not name or not password:
        return jsonify({"error": "email, name y password son obligatorios"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "El correo ya está registrado"}), 409

    u = User(email=email, name=name, role=role)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    return jsonify({"id": u.id, "email": u.email, "name": u.name, "role": u.role}), 201

@bp.route("/users/<int:user_id>", methods=["PUT"])
@admin_required
def update_user_admin(user_id):
    u = User.query.get(user_id)
    if not u:
        return jsonify({"error": "Usuario no encontrado"}), 404

    data = request.get_json() or {}
    if "name" in data:
        u.name = data.get("name", u.name)
    if "email" in data:
        if data["email"] != u.email and User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "El correo ya está registrado"}), 409
        u.email = data.get("email", u.email)
    if "password" in data and data.get("password"):
        u.set_password(data["password"])
    if "role" in data:
        u.role = data.get("role", u.role)

    db.session.commit()
    return jsonify({"id": u.id, "email": u.email, "name": u.name, "role": u.role}), 200

@bp.route("/users/<int:user_id>", methods=["DELETE"])
@admin_required
def delete_user(user_id):
    u = User.query.get(user_id)
    if not u:
        return jsonify({"error": "Usuario no encontrado"}), 404
    db.session.delete(u)
    db.session.commit()
    return jsonify({"message": "Usuario eliminado"}), 200
