from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/hello/<name>')
def hello(name):
    return render_template('user.html', user=name)

if __name__ == '__main__':
    app.run() 