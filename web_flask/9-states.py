#!/usr/bin/python3
""" web app flask to route all cities in list """
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close(self):
    """ function run when script is end """
    storage.close()


@app.route('/states')
def states():
    """ function that get all states route """
    return render_template("7-states_list.html", data=storage.all(State))


@app.route('/states/<id>')
def states_id(id):
    """ function that get all cities or states route """
    data = storage.all(State)
    obj = {}
    for st in data.values():
        if id == st.id:
            obj = st
            break
    return render_template("9-states.html", obj=obj)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
