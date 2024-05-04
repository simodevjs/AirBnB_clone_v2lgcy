#!/usr/bin/python3
"""
Description:
    Flask web application
"""
from models import storage, State
from flask import Flask, render_template


app = Flask(__name__)


@app.teardown_appcontext
def teardown(self) -> None:
    """close the session"""
    storage.close()


@app.route("/states_list", strict_slashes=False)
def states_list():
    """route to all states
    """
    state_obj = storage.all(State)
    states = [state_obj[key] for key in state_obj]
    return(render_template("7-states_list.html", states=states))


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)
