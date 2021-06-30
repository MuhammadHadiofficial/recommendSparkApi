from flask import  render_template,request,jsonify
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from . import db
from flask_login import login_required, current_user

from flask import Blueprint,render_template, redirect, url_for,request,flash
# from . import db
from werkzeug.security import generate_password_hash, check_password_hash
# from .models import User
from flask_login import login_user,logout_user,login_required
# from .models import User
# auth = Blueprint('auth', __name__)
# create a Flask instance
# and create a Flask-RESTful API instance with the created Flask instance
app = Flask(__name__)
db = SQLAlchemy()
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@162.222.180.69/recommendationSystem'
   
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from flask_login import UserMixin
class User(UserMixin,db.Model):
    userId = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    Email = db.Column(db.String(255), unique=True)
    Password = db.Column(db.String(255))
    userName = db.Column(db.String(255))
    Region = db.Column(db.String(255))
    def get_id(self):
        return (self.userId)
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(Email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('signup'))
    result=db.engine.execute(f'SELECT *  from user as U order by CAST(U.userId AS UNSIGNED) desc limit 1')
    userid=[row for row in result]
    # print(int(userid[0][0])+1)
    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(Email=email, userName=name, Password=password, userId=int(userid[0][0])+1)
    print(new_user)
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')

    remember = True if request.form.get('remember') else False
    
    user = User.query.filter_by(Email=email).first()
    password = request.form.get('password')
    print(email,password,user.Password)
    print(password,user.Password,type(user.Password),type(password),str(user.Password).strip()==str(password).strip())
    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    
    if not user or not user.Password.strip()==password.strip():
        flash('Please check your login details and try again.')
        return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page
    login_user(user, remember=remember)
    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('profile'))




def decode_sentiment(score, include_neutral=True):
    if include_neutral:        
        label = NEUTRAL
        if score <= SENTIMENT_THRESHOLDS[0]:
            label = NEGATIVE
        elif score >= SENTIMENT_THRESHOLDS[1]:
            label = POSITIVE

        return label
    else:
        return NEGATIVE if score < 0.5 else POSITIVE

def predict(text, include_neutral=True):
    
    return {"label": "label", "score":" float(score)",
       "elapsed_time": "time.time()-start_at"} 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def profile():
    # print(f'SELECT * FROM recommendationSystem.RATINGS join MOVIES on userId={current_user.userId} where {current_user.userId}=userId;')
    result = db.engine.execute(f'SELECT M.genre,M.title,R.prediction FROM MOVIES M  INNER JOIN RECOMMENDATIONS R ON M.ID  = R.movieId INNER JOIN user U on U.userId = R.userId  where U.userId = {current_user.userId} ORDER BY R.prediction desc LIMIT 10')
    print(f'SELECT U.userName,M.title,R.rating FROM MOVIES M  INNER JOIN RATINGS R ON M.ID  = R.movieId INNER JOIN user U on U.userId = R.userId  where U.userId = {current_user.userId} ORDER BY R.rating desc')
    names = [row for row in result]
    print(names)
    result2=db.engine.execute(f'SELECT distinct(title),id FROM recommendationSystem.MOVIES ;')
    movie=[row for row in result2]
    return render_template('profile.html',user=current_user,recommendation=names, movies=movie)

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', '',)
    id = request.args.get('id', '',)
    user = request.args.get('user', '',)
    print(a)
    print(id)
    print(user)
    result2=db.engine.execute(f'insert RATINGS values ({user},{id},{a});')
    # print("received")
    # result=    predict(a)
    # print(result)    
    result="success"
    return jsonify(result)



if __name__ == '__main__':

    
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(user_id)
    # run the Flask RESTful API, make the server publicly available (host='0.0.0.0') on port 8080
    app.run(host='0.0.0.0', port=8080, debug=True)