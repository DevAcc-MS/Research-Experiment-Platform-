from flask import Blueprint

gaming_bp = Blueprint('gaming_bp', __name__, template_folder='templates')

from . import gaming_controller