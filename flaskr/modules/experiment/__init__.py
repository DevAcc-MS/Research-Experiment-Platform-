from flask import Blueprint

experiment_bp = Blueprint('experiment_bp', __name__, template_folder='templates')

from . import experiment_controller