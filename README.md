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
- simply run `python app.py`
- you should have your app served up on `http://127.0.0.1:5000/` by default

#### [Dev Only] Populate Database with Fake test data

```bash
$ flask shell
>>> from app import fake
>>> fake.user() # to create a bounch of fake users
>>> fake.post() # to create a bounch of fake posts
```

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