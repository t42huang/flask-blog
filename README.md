# Flask Blog

## Notes on Setup

### Prerequisites

- Note: the commands in this instruction are for Mac OS, other OS users might need to find equivalent commands to run
- have this repository, either via git clone or download & unzip
- have python3 installed
- navigiate to this repo, create a virtual environment: `python3 -m venv venv`, where the 2ed `venv` is the name of the virtual environment
- activate this virtual environment: `source venv/bin/activate`, you should have `(venv)` prefix at your terminal prompt. (BTW, to deactivate it, simply run `deactivate`)
- install `Flask` in this virtual environment: `pip install flask`
- install `Bootstrap`: `pip install flask-bootstrap`

### To have the app up running

- simply run `python app.py`
- you should have your app served up on `http://127.0.0.1:5000/` by default

## Notes on Flask

### command-line options

- `flask --help`: run this to read more about the flask command-line options

- `export FLASK_APP="index.py"`
- `flask run`: this will run the app with a dev server

- `flask run --help` to read more about options available for `flask run`
- `flask run --host 0.0.0.0`: The dev web server listens to localhost network interface by default, which means only connections and requests originated from this computer will be accepted. By specifying the host to `0.0.0.0`, this asks the dev web server to listen for connections and requests on the public network interface, which means other devices (e.g. your phone, another computer) connected to the same network (e.g. wifi) will be able to visit this app via your computer's ip address and port, e.g. `http://192.168.0.16:5000`

### Flask Extensions

- Jinja2 template engine
- Bootstrap frontend framework

## Reference

- Book: Flask Web Development - Developing Web Applications with Python, second edition, by Miguel Grinberg