from flask import Blueprint

nongaming_bp = Blueprint('nongaming_bp', __name__, template_folder='templates')

from . import nongaming_controller