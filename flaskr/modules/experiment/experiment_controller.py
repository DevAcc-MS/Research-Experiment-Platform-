from flask import render_template, request, redirect
from flask.helpers import url_for

from . import experiment_bp
from flaskr.models import ActivePassiveVideo

@experiment_bp.route("/")
def index():
    # print (url_for('map_plot_bp.index'))
    return render_template('experiment/base.html')


@experiment_bp.route("/consentForm")
def consentForm():
    return render_template('experiment/consentForm.html')

@experiment_bp.route("/participantVideo", methods=['POST', 'GET'])
def participantVideo():
    participantId = "---"
    ytURL = ""
    if request.method == 'POST':
        participantId = request.form.get('participantId')
        # if len(participantId) < 4: could be greater than 4, For ex: AG100
        #     print("Handle Error\n") 
        if participantId[0] == 'P' or participantId[0] == 'p':
            return redirect("/experiment/passive/" + participantId)
        elif participantId[0] == 'A' or participantId[0] == 'a':
            return redirect("/experiment/active/" + participantId)
        
        # Handle Error
        # ret = ActivePassiveVideo.query.filter_by(passiveId=participantId).first()
        # if ret is not None:
        #     ytURL = ret.ytURL
        # print(ytURL)
        
    #Passerror parameter
    return render_template('experiment/participantVideo.html', ytURL=ytURL)


@experiment_bp.route("/passive/<string:pId>", methods=['POST', 'GET'])
def passiveMode(pId):
    return render_template("experiment/passive.html")

@experiment_bp.route("/active/<string:pId>", methods=['POST', 'GET'])
def activeMode(pId):
    return render_template("experiment/active.html")


@experiment_bp.route("/testPhase", methods=['POST', 'GET'])
def testPhase():
    return render_template("experiment/testPhase.html")


@experiment_bp.route("/thankyou")
def thankyou():
    return render_template('experiment/thankyou.html')