from flask import render_template, request, session, flash, redirect
from main import app
from applications.models import *

@app.route('/')
def index():
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

        return render_template('home.html')
    
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


