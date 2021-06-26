from flask import render_template, request, redirect
from flask.helpers import url_for

import os
from . import nongaming_bp
from flaskr import app
from flaskr.models import db, ActivePassiveVideo, NonGaming
from werkzeug.utils import secure_filename

@nongaming_bp.route("/")
def index():
    # print (url_for('map_plot_bp.index'))
    return render_template('nongaming/base.html')


def getId():
    tmp = NonGaming.query.all()
    Id = 1
    while True:
        flag = True
        for tt in tmp:
            if tt.pId == Id:
                flag = False
                break
        if flag == True:
            break
        Id = Id + 1
    return Id

@nongaming_bp.route("/consentForm")
def consentForm():
    pId = 'NG' + str(getId())
    return render_template('nongaming/consentForm.html', pId = pId)

@nongaming_bp.route("/reminder", methods=['POST', 'GET'])
def gentlereminder():
    return render_template('nongaming/reminder.html')

@nongaming_bp.route("/participantVideo", methods=['POST', 'GET'])
def participantVideo():
    participantId = "---"
    ytURL = ""
    if request.method == 'POST':
        tId = getId()
        print("Id = " + str(tId))
        Id = 'G' + str(tId)
        # if len(participantId) < 4: could be greater than 4, For ex: AG100
        #     print("Handle Error\n") 
        if tId % 2 == 0:
            return redirect("/nongaming/passive/" + Id)
        else:
            return redirect("/nongaming/active/" + Id)
        
        # Handle Error
        # ret = ActivePassiveVideo.query.filter_by(passiveId=participantId).first()
        # if ret is not None:
        #     ytURL = ret.ytURL
        # print(ytURL)
        
    #Passerror parameter
    return render_template('nongaming/participantVideo.html', ytURL=ytURL)


@nongaming_bp.route("/passive/<string:pId>", methods=['POST', 'GET'])
def passiveMode(pId):
    return render_template("nongaming/passive.html")

@nongaming_bp.route("/active/<string:pId>", methods=['POST', 'GET'])
def activeMode(pId):
    return render_template("nongaming/active.html")


@nongaming_bp.route("/testPhase", methods=['POST', 'GET'])
def testPhase():
    return render_template("nongaming/testPhase.html")

@nongaming_bp.route("/testPhase2", methods=['POST', 'GET'])
def testPhase2():
    pId = 'NG' + str(getId())
    return render_template("nongaming/testPhase2.html", pId=pId)


@nongaming_bp.route("/fileUpload", methods=['POST', 'GET'])
def fileUpload():
    if request.method == 'POST':
        
        if 'mapImage' not in request.files or 'zippedFolder' not in request.files:
            return redirect(request.url_root)


        image = request.files['mapImage']
        imageName = secure_filename(image.filename)

        zipFile = request.files['zippedFolder']
        zipFileName = secure_filename(zipFile.filename)

        if image == None or zipFile == None or imageName == '' or zipFileName == '':
            print('Upload file missing')
            return redirect('/nongaming/fileUpload')

        Id = getId()
        imageName = 'NG' + str(Id) + '_' + imageName
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], imageName))

        zipFileName = 'NG' + str(Id) + '_' + zipFileName
        zipFile.save(os.path.join(app.config['UPLOAD_FOLDER'], zipFileName))
        
        participantData = NonGaming.query.filter_by(pId=Id).first() 

        print("participantData ->  ", participantData)

        if participantData == None:
            participantData = NonGaming(pId=Id, imageName=imageName, zipFileName=zipFileName)
            db.session.add(participantData)
            db.session.commit()
        else:
            participantData.imageName = imageName
            participantData.zipFileName = zipFileName
            db.session.commit()

        print(imageName + "\t---\t" + zipFileName)
        return redirect('/nongaming/selfreportQ')

    return render_template('nongaming/fileUpload.html')

@nongaming_bp.route("/selfreportQ", methods=['POST', 'GET'])
def selfreportQ():
    pId = 'NG' + str(getId() - 1)
    return render_template("nongaming/selfreportQ.html", pId=pId)

@nongaming_bp.route("/thankyou")
def thankyou():
    return render_template('nongaming/thankyou.html')