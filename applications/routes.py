from flask import render_template, request, session, flash, redirect, url_for
from main import app
from applications.models import *
from datetime import datetime

@app.route('/')
def index():
    if 'user_email' in session:
        categories = Categories.query.all()
        products = Products.query.all()
        return render_template('home.html', categories=categories, products=products)
    return render_template('home.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        email = request.form.get('email',None)
        password = request.form.get('password',None)

        #data validation
        if not email or not password:
            flash('Please enter email and password')
            return render_template('login.html')
        
        #check if user exists
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('User does not exist')
            return render_template('login.html')
        
        if user.password != password:
            flash('Incorrect password')
            return render_template('login.html')
        
        session['user_email'] = user.email
        session['user_role'] = user.roles[0].name
        flash('Login successful')

        return redirect(url_for('index'))
    
@app.route('/logout')
def logout():
    session.pop('user_email', None)
    session.pop('user_role', None)
    flash('Logged out')
    return render_template('home.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html') 
    
    if request.method == 'POST':
        email = request.form.get('email',None)
        password = request.form.get('password',None)
        confirm_password = request.form.get('confirm_password',None)
        address = request.form.get('address',None)
        role = request.form.get('role',None)

        #data validation
        if not email or not password or not confirm_password or not role or not address:
            flash('Please enter all fields')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match')
            return render_template('register.html')
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long')
            return render_template('register.html')
        
        #check if user exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('User already exists')
            return render_template('register.html')
        
        role_object = Role.query.filter_by(name=role).first()
        if not role_object:
            flash('Invalid role')
            return render_template('register.html')
        
        user = User(email= email,
                    password = password,
                    address = address,
                    roles = [role_object])
        db.session.add(user)
        db.session.commit()

        flash('User registered successfully')
        return redirect('/login')

@app.route('/add_category', methods=['GET','POST'])
def add_category():
    if request.method == 'GET':
        return render_template('add_category.html')
    
    if request.method == 'POST':
        name = request.form.get('name',None)
        description = request.form.get('description',None)

        #data validation
        if not name:
            flash('Please enter category name')
            return render_template('add_category.html')
        
        category = Categories.query.filter_by(name=name).first()
        if category:
            flash('Category already exists')
            return render_template('add_category.html')
        
        category = Categories(name=name, decsription=description)
        db.session.add(category)
        db.session.commit()

        flash('Category added successfully')
        return redirect(url_for('index'))


@app.route('/add_product', methods=['GET','POST'])
def add_product():
    if request.method == 'GET':
        categories = Categories.query.all()
        return render_template('add_product.html', categories=categories)
    
    if request.method == 'POST':
        name = request.form.get('name',None) 
        selling_price = request.form.get('selling_price',None)
        cost_price = request.form.get('cost_price',None)
        stock = request.form.get('stock',None)
        category_id = request.form.get('category',None)
        mfg_date = request.form.get('mfg_date',None)
        exp_date = request.form.get('expiry_date',None)
        # name = request.form['name'] 
        # 

        mfg_date = datetime.strptime(mfg_date, '%Y-%m-%d')
        exp_date = datetime.strptime(exp_date, '%Y-%m-%d')

        #data validation
        if not name or not selling_price or not cost_price or not stock or not category_id or not mfg_date or not exp_date:
            flash('Please enter all fields')
            return render_template('add_product.html')
                
        product = Products.query.filter_by(name=name).first()
        if product:
            flash('Product already exists')
            return render_template('add_product.html')
        
        # if exp_date < datetime.now():
        #     flash('Expiry date cannot be in the past')
        #     return render_template('add_product.html')
        category = Categories.query.get(category_id)
        if not category:
            flash('Invalid category')
            return render_template('add_product.html')
        
        product = Products(name=name,
                            selling_price=selling_price,
                            cost_price=cost_price,
                            stock=stock,
                            manufactering_date=mfg_date,
                            expiry_date=exp_date,
                            category_id=category_id)
        
        db.session.add(product)
        db.session.commit()

        flash('Product added successfully')
        return redirect(url_for('index'))
