from applications.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)

    roles = db.relationship('Role', secondary='user_role')

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(100), nullable = False, unique = True)
    decsription = db.Column(db.String(100), nullable = True)

    products = db.relationship('Products', backref = 'category', lazy = True)

class Products(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(100), nullable = False, unique = True)
    selling_price = db.Column(db.Float, nullable = False)
    cost_price = db.Column(db.Float, nullable = False)
    stock = db.Column(db.Integer, nullable = False)
    manufactering_date = db.Column(db.Date, nullable = False)
    expiry_date = db.Column(db.Date, nullable = False)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable = False)

class CategoryRequests(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    requester = db.Column(db.String(80), db.ForeignKey('user.id'))
    request_type = db.Column(db.String(80), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable = True)
    request_date = db.Column(db.Date, nullable=False)
    new_category_name = db.Column(db.String(80), nullable=True)
    new_category_description = db.Column(db.String(255), nullable=True)
    request_status = db.Column(db.String(80), nullable=False)

    category = db.relationship('Categories', lazy = True)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


