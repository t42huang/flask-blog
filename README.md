# Flask Blog

## Demo

An example of this project is deployed at [Tina's Flask Blog](https://tinasflaskblog.herokuapp.com/).

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
- config environment variables: 
  - if you need `.env` and/or `.env-mysql` file, you can based off yours from `template.env` and `template.env-mysql`
  - These 2 template files contains the environment variables needed as key value pairs
  - Change the values as you needed
  - At least you need to change the emails, smtp, passwords and the secret key

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

# create a heroku app
$ heroku create <appname>
Creating <appname>... done
https://<appname>.herokuapp.com/ | https://git.heroku.com/<appname>.git

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
$ heroku config:set FB_SECRET_KEY=f22ff38135b147b7836de9cdee05a556

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

After restart the deployment, you can play around with the app at `https://<appname>.herokuapp.com`.

### Check app logs

```bash
$ heroku logs
$ heroku logs --tail
```

### Upgrade or Maintainance

After the app is deployed and people are using the app, during an upgrade or maintainance, we can take the app offline to avoid unexpected user experience:

```bash
$ heroku maintenance:on
$ git push heroku master
$ heroku run flask deploy
$ heroku restart
$ heroku maintenance:off
```

During the maintenance, the user will see a static page indicating the app is offline for maintenance:

> Offline for maintenance
> This app is undergoing maintenance right now.
> 
> Please check back later.

## Docker

```bash
# add permission to execute on boot.sh
chmod +x boot.sh

# build the docker image
docker build -t flaskblog:latest .

# run the docker image (flask:latest) 
#   with customized name (flaskblog), in detached mode (-d), 
#   mapping port 8000 on host computer to docker image port 5000, 
#   with some environment variables (-e)
docker run \
--name flaskblog \
-d \
-p 8000:5000 \
-e FB_SECRET_KEY=<your-secret-key> \
-e MAIL_SERVER=<your-smtp-server> \
-e MAIL_USERNAME=<your-smtp-email> \
-e MAIL_PASSWORD=<your-smtp-email-password> \
-e FLASKBLOG_SENDER='Flask Blog Admin <your-admin-email>' \
-e FLASKBLOG_ADMIN=<your-admin-email> \
flaskblog:latest

# check docker app running status
docker ps -a
# if it's running, you can test this app by going to
# - http://localhost:8000, or http://0.0.0.0:8000
# - httt://your-ip-address:8000 from another device in the same network
```

### Push container to external registry

You can host your images to Docker's image repository - Docker Hub registery.

```bash
# login docker with your docker account if you haven't
docker login # -i flag for login within terminal interactively

# tag the container
docker tag flaskblog:latest <your-dockerhub-username>/flaskblog:latest

# upload the image to Docker Hub
docker push <your-dockerhub-username>/flaskblog:latest
# The container image is now publicly available, and anybody can start a container based on it with the docker run command:
docker run --name flaskblog -d -p 8000:5000 \
<your-dockerhub-username>/flaskblog:latest
```

### Run seperate container for database

```bash
# run seperate container for database
docker run --name mysql -d \
-e MYSQL_RANDOM_ROOT_PASSWORD=yes \
-e MYSQL_DATABASE=flaskblog \
-e MYSQL_USER=flaskblog \
-e MYSQL_PASSWORD=<database-password> \
mysql/mysql-server:5.7
```

### Use docker composer to link containers

```bash
# use docker compose to build and run the containers for the app
docker-compose up -d --build

# when it is done, 
## 1. you can check if the app is working by visiting: 
# - http://localhost:8000, or http://0.0.0.0:8000
# - httt://your-ip-address:8000 from another device in the same network

## 2. you should have 2 linked containers running for the flaskblog app
docker ps
## one for the flaskblog app, e.g. flaskblog_flaskblog_1
## another for the mysql database, e.g. flaskblog_mysql_1

# You can double-check the database is working as expected:
# 1. run following commands to get the generated root password from log
docker logs flaskblog_mysql_1
# 2. copy the root password string from the logs

# 3. inspect the mysql container
docker exec -it flaskblog_mysql_1

# 4. log into the mysql database in the container
mysql -h localhost -u root -p
Enter password: # use the password copied from the docker logs

# 5. do whatever query is necessary for double checking
mysql> USE flaskblog;
mysql> SHOW TABLES;
mysql> SELECT * FROM USERS;
```

### Some other useful commands

```bash
# add alias to get your ip address
echo "export alias ip='ipconfig getifaddr en0'" >> ~/.bash_profile
source ~/.bash_profile

# check logs on the docker app flaskblog
docker logs flaskblog

# inspect the running container through a shell session
docker exec -it flaskblog sh
## note: to exit the shell, run command: `exit`

# stop the running container
docker stop flaskblog 

# remove the container from the system
docker rm flaskblog

# to stop and remove the container from the system in one go, run this
docker rm -f flaskblog

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