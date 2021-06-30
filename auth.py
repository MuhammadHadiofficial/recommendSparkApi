from flask import Blueprint,render_template, redirect, url_for,request,flash
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user,logout_user,login_required

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(Email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(Email=email, userName=name, Password=password)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')

    remember = True if request.form.get('remember') else False
    
    user = User.query.filter_by(Email=email).first()
    password = request.form.get('password')
    print(email,password,user.Password)
    print(password,user.Password,type(user.Password),type(password),str(user.Password).strip()==str(password).strip())
    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    result = db.engine.execute("select * from RATINGS")
    names = [row[0] for row in result]
    print(names)
    if not user or not user.Password.strip()==password.strip():
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
    login_user(user, remember=remember)
    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('main.profile'))


