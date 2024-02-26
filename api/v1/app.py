#!/usr/bin/python3
"""
starts a flask web application
"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os

host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def removed_db(exception):
    """
    remove every db session connection to the database
    db is been created in every subsequent calls
    """
    storage.close()

@app.errorhandler(404)
def handle_404(exception):
    """
    handles 404 errors, in the event that global error handler fails
    """
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': 'Not found'}
    return make_response(jsonify(message), code)


@app.errorhandler(400)
def handle_404(exception):
    """
    handles 400 errros, in the event that global error handler fails
    """
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
