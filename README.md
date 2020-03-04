# Flask Blog

## Notes on Setup

### Prerequisites

Note: the commands in this instruction are for Mac OS, other OS users might need to find equivalent commands to run

- have this repository, either via git clone or download & unzip
- have python3 installed
- navigiate to this repo, create a virtual environment: `python3 -m venv venv`, where the 2ed `venv` is the name of the virtual environment
- activate this virtual environment: `source venv/bin/activate`, you should have `(venv)` prefix at your terminal prompt. (BTW, to deactivate it, simply run `deactivate`)
- in this virtual environment, install `Flask` and other dependencies: `pip install flask`, for example:
  - `Bootstrap`: `pip install flask-bootstrap`
  - `Moment`: `pip install flask-moment`
  - `flask-wtf`: `pip install flask-wtf`
  - `SQLALchemy`: `pip install flask-sqlalchemy`
  - Alembic wrapper - `Flask-Migrate`: `pip install flask-migrate`
  - `Flask-Mail`: `pip install flask-mail`

### To have the app up running

- Mail related configuration - add the following into your `~/.bash_profile`:

```bash
export MAIL_SERVER=<Your Mail SMTP Server>
export MAIL_USERNAME=<Your Mail username>
export MAIL_PASSWORD=<Your Mail password>
export FLASKBLOG_SENDER='Flask Blog Admin <xxx@yyy.com>' # admin & email
export FLASKBLOG_ADMIN=xxx@yyy.com # admin's email
```

- in terminal, run `flask db upgrade` to setup database
- Run other commands

```bash
$ flask shell
>>> Role.insert_roles() # initialize all Roles
>>> User.add_self_follows() # for existing users, add themselves as followers
```

- simply run `python app.py`
- you should have your app served up on `http://127.0.0.1:5000/` by default

#### [Dev Only] Populate Database with Fake test data

```bash
$ flask shell
>>> from app import fake
>>> fake.users() # to create a bounch of fake users
>>> fake.posts() # to create a bounch of fake posts
```

### To test REST API

To test REST API, run the following example commands in the terminal (using your own `<email>` and `<password>`)

```bash
$ http --json --auth <email>:<password> GET http://127.0.0.1:5000/api/v1/posts/

$ http --auth <email>:<password> --json POST \
> http://127.0.0.1:5000/api/v1/posts/ \
> "body=I'm adding a post from the *command line*."

$ # get auth token to avoid sending email and password for every single api request
$ http --auth <email>:<password> --json POST http://127.0.0.1:5000/api/v1/tokens/

$ # using the auth token obtained above
$ http --json --auth eyJhbGciOiJIUzUxMiI...: GET http://127.0.0.1:5000/api/v1/posts/
```

### To Get Test Coverage

```bash
$ export FBLOG_COVERAGE=1 # to persist this config, add it in your ~/.bash_profile

$ flask test --coverage
```

## Deploy on Heroku

```bash
# create your own free heroku account, then log in from the terminal:
$ heroku login -i

# create postgresql database
$ heroku addons:create heroku-postgresql:hobby-dev

# configure your heroku environment, all of them can be configured in .env file with format "KEY=value"
$ heroku config:set FLASK_APP=flaskblog.py
$ heroku config:set FLASK_CONFIG=heroku

$ ## for added security, config a secret key for production env, e.g.
### first, you need to have a secure secret string 
### you can obtain one using python, e.g.
$ python -c "import uuid; print(uuid.uuid4().hex)" 
f22ff38135b147b7836de9cdee05a556
### configure your heroku account using your secret key, e.g.
$ heroku config:set SECRET_KEY=f22ff38135b147b7836de9cdee05a556

# EMAIL & SMTP configs
heroku config:set MAIL_SERVER=<YOUR_MAIL_SERVER>
heroku config:set MAIL_USERNAME=<YOUR_MAIL_USERNAME>
heroku config:set MAIL_PASSWORD=<YOUR_MAIL_PASSWORD>

heroku config:set FLASKBLOG_SENDER=<YOUR_FLASKBLOG_SENDER>
heroku config:set FLASKBLOG_ADMIN=<YOUR_FLASKBLOG_ADMIN>
```

### deploy locally

```bash
# run deploy(), which includes create db, flask upgrade 
$ heroku local:run flask deploy
blablabla # setup configs, run deploy(), which includes create db, flask upgrade db, etc.

# get the app runing
$ heroku local
blablabla Listening at: http://0.0.0.0:5000 blablabla

# to use multiple dynos to scale the app locally
$ heroku local web=3
```

### deploy to heroku

```bash
# first, commit all changes (to master branch) needed for this deployment

# then push (master branch) to heroku
$ git push heroku master

# run deploy(), which includes create db, flask upgrade 
$ heroku run flask deploy

# restart the app so it runs with updated database setup
$ heroku restart

```

## TODOs

- Performance - Source Code Profiling doesn't work yet


## Notes on Flask

### command-line options

- `flask --help`: run this to read more about the flask command-line options

- `export FLASK_APP="flaskblog.py"`
- `flask run`: this will run the app with a dev server

- `flask run --help` to read more about options available for `flask run`
- `flask run --host 0.0.0.0`: The dev web server listens to localhost network interface by default, which means only connections and requests originated from this computer will be accepted. By specifying the host to `0.0.0.0`, this asks the dev web server to listen for connections and requests on the public network interface, which means other devices (e.g. your phone, another computer) connected to the same network (e.g. wifi) will be able to visit this app via your computer's ip address and port, e.g. `http://192.168.0.16:5000`

### Flask Extensions

- Jinja2 template engine [Documentation](https://jinja.palletsprojects.com/en/2.11.x/)
- Bootstrap frontend framework [Documentation](https://getbootstrap.com/docs/4.3/getting-started/introduction/)
- Moment for datetime transformations [Documentation](https://momentjs.com/docs/#/displaying/)
- WTForms [Documentation](https://wtforms.readthedocs.io/en/stable/)
- SQLALchemy [Documentation](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- Flask-Migrate [Documentation](https://flask-migrate.readthedocs.io/en/latest/)
- Flask-Mail [Documentation](https://pythonhosted.org/flask-mail/)
- Werkzeug for Password hashing and verification (alternatives: bcrypt, Passlib)
- Flask-Login
- itsdangerous
- packages to enable Markdown Rich-Text blog post: Flask-Pagedown, Markdown, bleach

#### Extensions for Dev

- Flask-Fake

## Notes

- Check cookie session using [JSON Web Tokens](https://jwt.io/)
- Obtain all dependencies: `pip freeze >requirements.txt`
- [Python UnitTest](https://docs.python.org/3.6/library/unittest.html)

## Reference

- Book: Flask Web Development - Developing Web Applications with Python, second edition, by Miguel Grinberg