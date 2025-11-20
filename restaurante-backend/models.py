from datetime import datetime
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default="client", index=True)  # 'admin' or 'client'
    orders = db.relationship("Order", backref="user", lazy="dynamic")

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {"id": self.id, "email": self.email, "name": self.name, "role": self.role}

    def __repr__(self):
        return f"<User {self.email}>"


class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255))
    category = db.Column(db.String(50), nullable=False, index=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False, index=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "image_url": self.image_url,
            "category": self.category,
            "is_active": self.is_active,
        }

    def __repr__(self):
        return f"<MenuItem {self.name}>"


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_item.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    menu_item = db.relationship("MenuItem", lazy=True)

    def to_dict(self):
        return {
            "id": self.menu_item_id,
            "name": self.menu_item.name if self.menu_item else None,
            "price": self.price,
            "quantity": self.quantity,
            "image": self.menu_item.image_url if self.menu_item else None,
            "category": self.menu_item.category if self.menu_item else None,
        }


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    status = db.Column(db.String(50), nullable=False, default="Recibido", index=True)
    pabellon = db.Column(db.String(100))
    mensaje = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    items = db.relationship("OrderItem", backref="order", cascade="all, delete-orphan", lazy="joined")

    def to_dict(self):
        return {
            "id": self.id,
            "user_name": self.user.name if self.user else "Usuario desconocido",
            "total_price": self.total_price,
            "created_at": self.created_at.isoformat(),
            "status": self.status,
            "pabellon": self.pabellon,
            "mensaje": self.mensaje,
            "item_count": len(self.items),
        }

    def to_detailed_dict(self):
        return {
            "id": self.id,
            "user_name": self.user.name if self.user else "Usuario desconocido",
            "total_price": self.total_price,
            "created_at": self.created_at.isoformat(),
            "status": self.status,
            "pabellon": self.pabellon,
            "mensaje": self.mensaje,
            "items": [it.to_dict() for it in self.items],
        }

    def __repr__(self):
        return f"<Order {self.id} - {self.status}>"
