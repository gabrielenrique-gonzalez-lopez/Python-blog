from flask import render_template, url_for, flash, redirect, session, g
from . import app
from werkzeug.security import check_password_hash, generate_password_hash
from .forms import RegistrationForm, LoginForm
from .db import get_db


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    db = get_db()
    if form.validate_on_submit():
        if db.execute('SELECT id FROM user WHERE username ?', (form.username.data)).fetchone() is not None:
            flash(f'User {form.username.data} is already registered.', 'danger')
        else:
            db.execute('INSERT INTO user (username, email, password) VALUES (?, ?)', (form.username.data, form.email.data, generate_password_hash(form.password.data)))
            db.commit()
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    db = get_db()
    if form.validate_on_submit():
        user = db.execute('SELECT * FROM user WHERE username = ?', (form.email.data)).fetchone()
        if user is None:
            flash('Login Unsuccessful. Please check username and password', 'danger')
        elif not check_password_hash(user['password'], form.password.data):
            flash('Login Unsuccessful. Please check password', 'danger')
        else:
            session.clear()
            session['user_id'] = user['id']
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
            
    return render_template('login.html', title='Login', form=form)