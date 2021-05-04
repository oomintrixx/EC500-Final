from flask import Blueprint

auth = Blueprint('file', __name__)

from . import views
