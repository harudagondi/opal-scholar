from app import app, db
from .models import User
from .forms import UsernameForm
from flask import Flask, redirect, url_for, render_template
from flask.ext.login import LoginManager, UserMixin, login_user, logout_user,\
    current_user
from .oauth import OAuthSignIn

lm = LoginManager(app)
lm.login_view = 'index'

@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    return render_template("home.html",
                           title="Home")

@app.route("/about")
def about():
    return render_template("about.html",
                           title="About")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = UsernameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        user.username = form.username.data
        db.session.commit()
    return render_template("login.html",
                           title="Login",
                           form=form)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, name = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, name=name)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('login'))
