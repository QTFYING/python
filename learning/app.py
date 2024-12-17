# app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/user/<name>')
def hello(name):
    return render_template('index.html', title="Flask Demo", name=name)

if __name__ == '__main__':
    app.run(debug=True)
