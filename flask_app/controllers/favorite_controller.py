from flask import render_template, redirect, request, session, flash, jsonify
from flask_app import app

from flask_bcrypt import Bcrypt  # Only needed on routes related to login/reg
bcrypt = Bcrypt(app)

# Import Your Models as Classes into the Controller to use their Classmethods

# from flask_app.models.table_model import classname
from flask_app.models.favorite_model import Favorite
from flask_app.models.user_model import User


# ====================================
#    Create Routes
#    Show Form Route, Submit Form Route
# ====================================

@app.route('/explore')
def explore_space():

    if 'user_id' not in session:
        flash('Please Sign in.')
        return redirect('/')

    one_user = User.get_user_by_id({'user_id': session['user_id']})
    return render_template('explore.html', one_user=one_user)

@app.route('/pod')
def space_pod():

    if 'user_id' not in session:
        flash('Please Sign in.')
        return redirect('/')

    one_user = User.get_user_by_id({'user_id': session['user_id']})
    return render_template('POD.html', one_user=one_user)

@app.route('/explore/favorite/<date>', methods=['POST'])
def favorite_space(date):

    favorite_data = {
        'date': date,
        'user_id': session['user_id']
    }
    Favorite.create_favorite(favorite_data)
    return 'successfully favorited'



# ====================================
# Log In Validations Route
# ====================================


# ====================================
#    Read Routes
#    Show Routes (Get All and Get One)
# ====================================

@app.route('/favorites/<int:favorite_id>')
def show_favorite(favorite_id):
    if 'user_id' not in session:
        flash('Please Sign in.')
        return redirect('/')
    
    one_user = User.get_user_by_id({'user_id': session['user_id']})
    one_favorite = Favorite.get_one_favorite({'favorite_id': favorite_id})
    
    return render_template('view.html', one_user=one_user, one_favorite=one_favorite)

# ====================================
#    Update Routes
#    Update Form Route, Submit Update Form Route
# ====================================


# ====================================
#    Delete Routes
# ====================================
@app.route('/favorite/delete/<int:favorite_id>')
def delete_one_favorite(favorite_id):

    Favorite.delete_favorite({'favorite_id': favorite_id})

    return redirect('/dashboard')