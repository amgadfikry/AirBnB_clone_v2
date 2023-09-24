#!/usr/bin/python3
""" web app flask to route all cities in list """
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close(self):
    """ function run when script is end """
    storage.close()


@app.route('/hbnb_filters')
def states():
    """ function that get all states route """
    state = storage.all(State)
    amenity = storage.all(Amenity)
    return render_template("10-hbnb_filters.html", state=state, amenity=amenity)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)