from flask import Blueprint, render_template, redirect, request, g, abort
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

from career_connections.database.models import PendingUser, User
from career_connections.utils.auth import login, logout

unauth_views_bp = Blueprint('unauthenticated_views', __name__)

class SigninForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')

class SignupForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email')

@unauth_views_bp.route('/')
def home():
    signin_form = SigninForm()
    signup_form = SignupForm()
    return render_template('signin.j2', login_form=signin_form, signup_form=signup_form)

@unauth_views_bp.route('/signin', methods=['POST'])
def signin():
    form = SigninForm()

    if form.username.data is None or form.password.data is None:
        return redirect('/?signin=invalid')

    if login(form.username.data, form.password.data):
        return redirect('/dashboard')

    return redirect('/?signin=invalid')

@unauth_views_bp.route('/signup', methods=['POST'])
def signup():
    form = SignupForm()

    pending_user = PendingUser(
        first_name=form.first_name.data,
        last_name=form.last_name.data,
        email=form.email.data)

    print(pending_user.to_dict())
    g.db.add(pending_user)
    g.db.commit()

    return redirect('/?signup=sucess')

@unauth_views_bp.route('/signout')
def signout():
    logout()
    return redirect('/')
