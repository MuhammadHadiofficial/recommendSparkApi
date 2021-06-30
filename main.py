from flask import Blueprint, render_template,request,jsonify
from . import db
from flask_login import login_required, current_user
import pickle

import time
main = Blueprint('main', __name__)


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
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def profile():
    print(f'SELECT * FROM recommendationSystem.RATINGS join MOVIES on userId={current_user.userId} where {current_user.userId}=userId;')
    result = db.engine.execute(f'select * from RATINGS as rt JOIN MOVIES on rt.userId={current_user.userId} where {current_user.userId}=rt.userId')
    print(result)
    names = [row[0] for row in result]
    print(names)
    return render_template('profile.html',name=current_user.userName)

@main.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', '',)
    print(a)
    result=    predict(a)
    print(result)    
    return jsonify(result)