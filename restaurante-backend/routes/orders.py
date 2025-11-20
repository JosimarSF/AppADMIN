from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils import admin_required
from .. import db
from ..models import Order, OrderItem, MenuItem

bp = Blueprint("orders", __name__)

@bp.route("/orders", methods=["GET"])
@jwt_required()
def get_orders_history():
    user_id = int(get_jwt_identity())
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    return jsonify([o.to_detailed_dict() for o in orders]), 200

@bp.route("/orders", methods=["POST"])
@jwt_required()
def create_order():
    data = request.get_json() or {}
    items = data.get("items", [])
    pabellon = data.get("pabellon")
    mensaje = data.get("mensaje")

    if not items:
        return jsonify({"error": "No hay productos"}), 400

    total = 0
    for item in items:
        try:
            total += float(item["price"]) * int(item["quantity"])
        except Exception:
            return jsonify({"error": "items mal formateados"}), 400

    new_order = Order(
        user_id=int(get_jwt_identity()),
        pabellon=pabellon,
        mensaje=mensaje,
        total_price=total,
    )
    db.session.add(new_order)
    db.session.flush()

    for item in items:
        db.session.add(
            OrderItem(
                order_id=new_order.id,
                menu_item_id=int(item["id"]),
                quantity=int(item["quantity"]),
                price=float(item["price"]),
            )
        )

    db.session.commit()
    return jsonify({"message": "Pedido creado correctamente", "order_id": new_order.id}), 201

@bp.route("/admin/orders", methods=["GET"])
@admin_required
def admin_orders():
    status = request.args.get("status")
    q = Order.query
    if status:
        q = q.filter_by(status=status)
    orders = q.order_by(Order.created_at.desc()).all()
    return jsonify([o.to_detailed_dict() for o in orders]), 200

@bp.route("/admin/orders/<int:order_id>/status", methods=["PUT"])
@admin_required
def admin_update_order_status(order_id):
    data = request.get_json() or {}
    new_status = data.get("status")
    if not new_status:
        return jsonify({"error": "status es obligatorio"}), 400
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Pedido no encontrado"}), 404
    order.status = new_status
    db.session.commit()
    return jsonify({"id": order.id, "status": order.status}), 200
