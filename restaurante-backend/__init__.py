import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(__file__ + "/.."))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "restaurant.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "una-clave-secreta-fuerte")

    CORS(app)
    db.init_app(app)
    jwt.init_app(app)

    # register blueprints
    from .routes.auth import bp as auth_bp
    from .routes.menu import bp as menu_bp
    from .routes.products_admin import bp as products_bp
    from .routes.users_admin import bp as users_bp
    from .routes.orders import bp as orders_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(menu_bp, url_prefix="/api")
    app.register_blueprint(products_bp, url_prefix="/api/admin")
    app.register_blueprint(users_bp, url_prefix="/api/admin")
    app.register_blueprint(orders_bp, url_prefix="/api")

    # create tables
    with app.app_context():
        db.create_all()

    return app
