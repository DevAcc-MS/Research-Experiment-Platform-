from flask import Blueprint

map_plot_bp = Blueprint('map_plot_bp', __name__, template_folder='templates')

from . import map_plot_controller

