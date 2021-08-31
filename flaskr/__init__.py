from flask import Flask, redirect
from flask.helpers import url_for
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy

from flaskr.models import ActivePassiveVideo, Gaming, NonGaming
from flaskr.modules import admin

app = Flask(__name__)

UPLOAD_FOLDER = './data/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:sharique1996@research.c3pp9ju22eal.ap-south-1.rds.amazonaws.com:3306/experiment'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from flaskr.models import db
db.init_app(app)

from flaskr.modules.admin import admin_bp
app.register_blueprint(admin_bp, url_prefix='/admin')

from flaskr.modules.map_plot import map_plot_bp
app.register_blueprint(map_plot_bp, url_prefix='/map_plot')

from flaskr.modules.nongaming import nongaming_bp
app.register_blueprint(nongaming_bp, url_prefix='/nongaming')

from flaskr.modules.gaming import gaming_bp
app.register_blueprint(gaming_bp, url_prefix='/gaming')

@app.route("/")
def hello_world():
    return redirect(url_for('nongaming_bp.index'))

@app.cli.command("resetdb")
def reset_db():
	db.drop_all()
	db.create_all()

@app.cli.command("addDummyUser")
def addDummyUser():
    temp = ActivePassiveVideo('A01', 'P01', 'https://www.youtube.com/embed/tgbNymZ7vqY', False, False)
    db.session.add(temp)
    db.session.commit()


@app.cli.command("showAllData")
def showAllData():
    print("Gaming:")
    allGaming = Gaming.query.all()
    for _ in allGaming:
        print(_)

    print("\nNon Gaming:")
    allNonGaming = NonGaming.query.all()
    for _ in allNonGaming:
        print(_)

@app.cli.command("removeFromNG")
def removeFromNG():
    dng = NonGaming.query.filter_by(pId=1).first()
    dng2 = NonGaming.query.filter_by(pId=3).first()
    print(dng)
    db.session.delete(dng)
    db.session.delete(dng2)
    db.session.commit()

@app.cli.command("removeFromG")
def removeFromG():
    # for id in range(2, 7, 2):
    #     dg = Gaming.query.filter_by(pId=id).first()
    #     if dg != None:
    #         db.session.delete(dg)
    ng = Gaming.query.filter_by(pId=7).first()
    ng2 = Gaming.query.filter_by(pId=9).first()

    db.session.delete(ng)
    db.session.delete(ng2)
    db.session.commit()
