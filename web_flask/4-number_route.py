#!/usr/bin/python3
""" flask web application """


from flask import Flask


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def home():
    """ route home function """
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb():
    """ route hbnb function """
    return "HBNB"


@app.route('/c/<text>')
def text(text):
    """ route text function """
    return "C {}".format(text.replace("_", " "))


@app.route('/python', defaults={"text": "is cool"})
@app.route('/python/<text>')
def python(text):
    """ route python function """
    return "Python {}".format(text.replace("_", " "))


@app.route('/number/<int:n>')
def number(n):
    """ number route function """
    return "{} is a number".format(n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
