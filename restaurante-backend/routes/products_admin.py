from flask import Blueprint, request, jsonify
from ..utils import admin_required
from .. import db
from ..models import MenuItem

bp = Blueprint("products_admin", __name__)

@bp.route("/products", methods=["GET"])
@admin_required
def list_products():
    items = MenuItem.query.order_by(MenuItem.category, MenuItem.name).all()
    return jsonify([i.to_dict() for i in items]), 200

@bp.route("/products", methods=["POST"])
@admin_required
def create_product():
    data = request.get_json() or {}
    name = data.get("name")
    price = data.get("price")
    category = data.get("category", "Sin categoría")

    if not name or price is None:
        return jsonify({"error": "name y price son obligatorios"}), 400

    try:
        price = float(price)
    except (ValueError, TypeError):
        return jsonify({"error": "price debe ser un número"}), 400

    item = MenuItem(
        name=name.strip(),
        description=data.get("description", ""),
        price=price,
        image_url=data.get("image_url"),
        category=category.strip(),
        is_active=bool(data.get("is_active", True))
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

@bp.route("/products/<int:item_id>", methods=["PUT"])
@admin_required
def update_product(item_id):
    item = MenuItem.query.get(item_id)
    if not item:
        return jsonify({"error": "Producto no encontrado"}), 404

    data = request.get_json() or {}
    if "name" in data and data["name"]:
        item.name = data["name"].strip()
    if "description" in data:
        item.description = data.get("description", item.description)
    if "price" in data:
        try:
            item.price = float(data["price"])
        except (ValueError, TypeError):
            return jsonify({"error": "price debe ser un número"}), 400
    if "image_url" in data:
        item.image_url = data.get("image_url")
    if "category" in data:
        item.category = data.get("category", item.category)
    if "is_active" in data:
        item.is_active = bool(data.get("is_active"))

    db.session.commit()
    return jsonify(item.to_dict()), 200

@bp.route("/products/<int:item_id>", methods=["DELETE"])
@admin_required
def delete_product(item_id):
    item = MenuItem.query.get(item_id)
    if not item:
        return jsonify({"error": "Producto no encontrado"}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Producto eliminado"}), 200

@bp.route("/products/<int:item_id>/toggle", methods=["PATCH"])
@admin_required
def toggle_product(item_id):
    item = MenuItem.query.get(item_id)
    if not item:
        return jsonify({"error": "Producto no encontrado"}), 404
    item.is_active = not item.is_active
    db.session.commit()
    return jsonify({"id": item.id, "is_active": item.is_active}), 200

@bp.route("/categories", methods=["GET"])
@admin_required
def get_categories():
    cats = db.session.query(MenuItem.category).distinct().all()
    categories = [c[0] for c in cats]
    return jsonify(categories), 200

@bp.route("/categories/rename", methods=["PUT"])
@admin_required
def rename_category():
    data = request.get_json() or {}
    old = data.get("old")
    new = data.get("new")
    if not old or not new:
        return jsonify({"error": "old y new son obligatorios"}), 400
    items = MenuItem.query.filter_by(category=old).all()
    for i in items:
        i.category = new
    db.session.commit()
    return jsonify({"message": "Categoría renombrada", "old": old, "new": new}), 200
