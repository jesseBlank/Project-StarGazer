from flask import render_template, redirect, request, session, flash
from flask_app import app

from flask_bcrypt import Bcrypt  # Only needed on routes related to login/reg
bcrypt = Bcrypt(app)

# Import Your Models as Classes into the Controller to use their Classmethods

# from flask_app.models.table_model import classname
from flask_app.models.user_model import User
from flask_app.models.favorite_model import Favorite

@app.route('/register')
def index():
    return render_template('index.html')

@app.route('/')
def login_page():
    return render_template('login.html')


# ====================================
#    Create Routes
#    Show Form Route, Submit Form Route
# ====================================

@app.route('/register_user', methods=['POST'])
def successful_register():

    if not User.validate_user(request.form):
        return redirect('/register')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }

    new_user_id = User.create_user(data)

    session['user_id'] = new_user_id

    return redirect('/dashboard')

# ====================================
# Log In Validations Route
# ====================================

@app.route('/loginuser', methods=['POST'])
def login_user():

    data = {'email' : request.form['email']}
    user_in_db = User.get_user_by_email(data)

    if not user_in_db:
        flash("Invalid email/password.")
        return redirect('/')

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid email/password.")
        return redirect('/')

    session['user_id'] = user_in_db.id

    return redirect('/dashboard')

@app.route('/logout')
def logout_user():
    session.clear()
    return redirect('/')


# ====================================
#    Read Routes
#    Show Routes (Get All and Get One)
# ====================================

@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        flash('Please Sign in.')
        return redirect('/')

    one_user = User.get_user_by_id({'user_id': session['user_id']})
    all_favorites = Favorite.get_all_favorites()

    return render_template('dashboard.html', one_user=one_user, all_favorites=all_favorites)


# ====================================
#    Update Routes
#    Update Form Route, Submit Update Form Route
# ====================================


# ====================================
#    Delete Routes
# ====================================