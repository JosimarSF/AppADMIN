import os
from app import create_app, db
from app.models import User

ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Admin2025")
ADMIN_NAME = os.environ.get("ADMIN_NAME", "Admin")

app = create_app()

with app.app_context():
    db.create_all()
    admin = User.query.filter_by(email=ADMIN_EMAIL).first()
    if admin:
        if admin.role != "admin":
            admin.role = "admin"
            db.session.commit()
            print("Usuario existente actualizado a admin:", ADMIN_EMAIL)
        else:
            print("Admin ya existe:", ADMIN_EMAIL)
    else:
        new_admin = User(email=ADMIN_EMAIL, name=ADMIN_NAME, role="admin")
        new_admin.set_password(ADMIN_PASSWORD)
        db.session.add(new_admin)
        db.session.commit()
        print("Admin creado:", ADMIN_EMAIL)
