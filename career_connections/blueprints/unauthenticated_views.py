from flask import Blueprint, render_template, redirect, request, g, abort, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField

from career_connections.database.models import PendingUser, User
from career_connections.utils.auth import login, logout, hash_password

unauth_views_bp = Blueprint('unauthenticated_views', __name__)

class SigninForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')

class SignupForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email')

class CreateAccountForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    invite_code = HiddenField()


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
        email=form.email.data,
        is_approved=False)

    g.db.add(pending_user)
    g.db.commit()

    return redirect('/?signup=sucess')

@unauth_views_bp.route('/signout')
def signout():
    logout()
    return redirect('/')


@unauth_views_bp.route('/create_account', methods=['GET'])
def create_account_form():
    code = request.args.get('code')
    user = g.db.query(PendingUser).filter(PendingUser.invite_code==code).one_or_none()
    if not user:
        return redirect('/?create_account=not_found')

    form = CreateAccountForm(invite_code=code)

    return render_template('create_account.j2', form=form)


@unauth_views_bp.route('/create_account', methods=['POST'])
def create_account():
    form = CreateAccountForm()
    pending_user = g.db.query(PendingUser).filter(PendingUser.invite_code==form.invite_code.data).one_or_none()
    if not pending_user:
        return redirect('/?create_account=not_found')

    user = User(
        username=form.username.data,
        password=hash_password(form.password.data),
        first_name=pending_user.first_name,
        last_name=pending_user.last_name,
        email=pending_user.email
    )

    g.db.add(user)
    g.db.delete(pending_user)
    g.db.commit()



    if login(form.username.data, form.password.data):
        return redirect('/dashboard')

    return redirect('/?create_account=not_found')
