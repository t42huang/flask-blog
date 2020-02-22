from flask import render_template, session, redirect, url_for, current_app, flash

from datetime import datetime

from . import main
from .forms import NameForm

from .. import db
from ..models import User
from ..email import send_email

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    
    if form.validate_on_submit():
        oldName = session.get('name')
        if oldName is not None and oldName != form.name.data:
            flash("Note: Your name is changed from {} to {}".format(oldName, form.name.data))
        
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if current_app.config['FLASKBLOG_ADMIN']:
                send_email(current_app.config['FLASKBLOG_ADMIN'], 'New User',
                    'mail/new_user', user=user)
        else:
            session['known'] = True
        
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    
    return render_template('index.html', 
        form=form, 
        name=session.get('name'), 
        known=session.get('known', False),
        current_time=datetime.utcnow())

@main.route('/hello/<name>')
def hello(name):
    return render_template('user.html', user=name)
