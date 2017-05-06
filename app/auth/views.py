from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User
from .forms import RegistrationForm,ChangePasswordForm,\
     PasswordResetRequestForm, PasswordResetForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST" and "username" in request.form and "password" in request.form:
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user is not None and user.verify_password(password):
            login_user(user)
            # return redirect(request.args.get('next') or url_for('main.index'))
            return redirect(url_for('main.index'))
        flash('Invalid username or password.')

    return render_template('auth/login_in.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()  #houjia
        token = user.generate_confirmation_token()
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)
