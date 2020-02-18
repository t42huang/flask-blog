from flask import Flask, render_template

from flask_bootstrap import Bootstrap
from flask_moment import Moment

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from datetime import datetime

app = Flask(__name__)
# add in a secret key for this app to avoid CSRF (Cross-Site Request Forgery) on forms
# for better security, remove secret key from source code, store it in an environment variable instead
app.config['SECRET_KEY'] = "Secret Key Hidden in Plain Sight LOL"

# Innitiate flask extensions
bootstrap = Bootstrap(app)
moment = Moment(app)

# define a simple form class with name field and submit button
class NameForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/')
def hello_world():
    form = NameForm()
    return render_template('index.html', form=form, current_time=datetime.utcnow())

@app.route('/hello/<name>')
def hello(name):
    return render_template('user.html', user=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500

if __name__ == '__main__':
    app.run() 