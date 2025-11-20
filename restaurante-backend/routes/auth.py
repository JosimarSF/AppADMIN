from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from .. import db
from ..models import User

bp = Blueprint("auth", __name__)

@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    if not email or not password or not name:
        return jsonify({"error": "Faltan datos"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "El correo ya está registrado"}), 409

    new_user = User(email=email, name=name)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuario creado exitosamente"}), 201

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Faltan datos"}), 400

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            "access_token": access_token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
            },
        }), 200

    return jsonify({"error": "Credenciales inválidas"}), 401
