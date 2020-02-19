import os
from threading import Thread

from flask import Flask, render_template, session, redirect, url_for, flash

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_mail import Message

from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# add in a secret key for this app to avoid CSRF (Cross-Site Request Forgery) on forms
# for better security, remove secret key from source code, store it in an environment variable instead
app.config['SECRET_KEY'] = "Secret Key Hidden in Plain Sight LOL"

# configure SQLAlchemy database instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

## Mail configs
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')

# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL'] = True

# app.config['MAIL_PORT'] = 587
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

# Innitiate flask extensions
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

# define a simple form class with name field and submit button
class NameForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

# database models
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

app.config['FB_MAIL_SUBJECT_PREFIX'] = '[Flask Blog]'
app.config['FB_MAIL_SENDER'] = os.environ.get('FLASKBLOG_SENDER')
app.config['FLASKBLOG_ADMIN'] = os.environ.get('FLASKBLOG_ADMIN')


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
    
def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FB_MAIL_SUBJECT_PREFIX'] + subject,
        sender=app.config['FB_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


@app.route('/', methods=['GET', 'POST'])
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
            if app.config['FLASKBLOG_ADMIN']:
                send_email(app.config['FLASKBLOG_ADMIN'], 'New User',
                    'mail/new_user', user=user)
        else:
            session['known'] = True
        
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    
    return render_template('index.html', 
        form=form, 
        name=session.get('name'), 
        known=session.get('known', False),
        current_time=datetime.utcnow())

@app.route('/hello/<name>')
def hello(name):
    return render_template('user.html', user=name)

@app.shell_context_processor
def prepare_shell_context():
    return dict(db=db, User=User, Role=Role)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500

if __name__ == '__main__':
    app.run() 