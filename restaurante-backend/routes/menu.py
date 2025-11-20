from flask import Blueprint, jsonify
from ..models import MenuItem

bp = Blueprint("menu", __name__)

@bp.route("/menu", methods=["GET"])
def get_menu():
    items = MenuItem.query.filter_by(is_active=True).order_by(MenuItem.category, MenuItem.name).all()
    if not items:
        return jsonify([]), 200
    categories = {}
    for item in items:
        categories.setdefault(item.category, []).append(item.to_dict())
    categorized = [{"title": c, "data": d} for c, d in categories.items()]
    return jsonify(categorized)
