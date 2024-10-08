from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from applications.config import Config
from applications.database import db
from applications.models import User, Role, UserRole

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name = 'admin')
            db.session.add(admin_role)
        store_manager = Role.query.filter_by(name='store_manager').first()
        if not store_manager:
            store_manager = Role(name = 'store_manager')
            db.session.add(store_manager)
        customer_role = Role.query.filter_by(name='customer').first()
        if not customer_role:
            customer_role = Role(name = 'customer')
            db.session.add(customer_role)

        admin_user = User.query.filter_by(email='admin@grocerystore.com').first()
        if not admin_user:
            admin_user = User(email='admin@grocerystore.com',
                              password='admin',
                              address='admin address',
                              roles = [admin_role])
            db.session.add(admin_user)
        db.session.commit()
    return app

app = create_app()

from applications.routes import *

if __name__ == '__main__':
    app.run(debug=True)
