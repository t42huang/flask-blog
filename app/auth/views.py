from flask import render_template, redirect, request, url_for, flash

from flask_login import login_user, login_required, logout_user, current_user

from . import auth
from .forms import LoginForm, RegistrationForm, \
    ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm, \
    ChangeEmailForm

from .. import db
from ..models import User
from ..email import send_email

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        
        flash('Invalid email or password')
    
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()

        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)

        flash("A confirmation email has been sent to your email, please confirm before you can sign in.")
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have successfully confirmed your account. You can sign in now.')
    else:
        flash('The confirmation link is invalid or has expired.')
    
    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))
    
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    
    send_email(current_user.email, 
        'Confirm Your Account',
        'auth/email/confirm',
        user=current_user,
        token=token
    )
    
    flash('A new confirmation email has been sent to you by email.')
    
    return redirect(url_for('main.index'))


@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email():
    form = ChangeEmailForm()

    if form.validate_on_submit():
        token = current_user.generate_change_email_token(form.email.data)
        send_email(current_user.email, 'Change your email',
            'auth/email/change_email',
            user=current_user, token=token, new_email=form.email.data
        )
        flash('A confirmation email has been sent to your original email regardng your request to change email.')
        return redirect(url_for('main.index'))

    return render_template('auth/change_email.html', form=form)

@auth.route('/change_email/<token>')
def confirm_change_email(token):
    user = User.change_email(token)
    if user:
        db.session.commit()
        send_email(current_user.email, 'Email Updated',
            'auth/email/email_updated',
            user=user
        )
        flash('Your Email has been updated. Please login with your new Email')
    else:
        flash('Something went wrong when changing your email, please contact your administrator regarding this issue.')
    return redirect(url_for('auth.login'))

@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated')
            
            return redirect(url_for('main.index'))

    return render_template('auth/change_password.html', form=form)


@auth.route('reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    
    form = PasswordResetRequestForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your password', 
                'auth/email/reset_password',
                user=user, token=token
            )

            flash('An email has been sent to you to reset your password')
            return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', form=form)

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    
    form = PasswordResetForm()
    
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your password has been updated')
        else:
            flash('Something went wrong on resetting your password, please contact your administrator for help.')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', form=form)