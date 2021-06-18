import os
from flask import render_template, request, flash
from werkzeug.utils import redirect, secure_filename

from . import map_plot_bp
from flaskr import app

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@map_plot_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url_root)
        file = request.files['file']
        if file.filename == '':
            print ('No file selectod')
            return redirect(request.url_root)

        if file:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                print(file.filename)
            else:
                print('Wrong file format')
        else:
            print("Enter valid file")

    return render_template('map_plot/base.html')