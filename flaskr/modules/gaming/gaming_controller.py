from flask import render_template, request, redirect
from flask.helpers import url_for

import os
from . import gaming_bp
from flaskr import app
from flaskr.models import db, ActivePassiveVideo, Gaming
from werkzeug.utils import secure_filename

@gaming_bp.route("/")
def index():
    # print (url_for('map_plot_bp.index'))
    return render_template('gaming/base.html')
def getId():
    tmp = Gaming.query.all()
    Id = 1
    while True:
        flag = True
        for tt in tmp:
            ''' To remove below if condition when doing for passive condition only'''
            if tt.pId % 2 == 0:
                continue
            if tt.pId == Id:
                flag = False
                break
        if flag == True:
            break
        Id = Id + 2
    return Id

@gaming_bp.route("/consentForm")
def consentForm():
    pId = 'G' + str(getId())
    return render_template('gaming/consentForm.html', pId=pId)

@gaming_bp.route("/reminder", methods=['POST', 'GET'])
def gentlereminder():
    return render_template('gaming/reminder.html')

@gaming_bp.route("/participantVideo", methods=['POST', 'GET'])
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
            return redirect("/gaming/passive/" + Id)
        else:
            return redirect("/gaming/active/" + Id)
        
        # Handle Error
        # ret = ActivePassiveVideo.query.filter_by(passiveId=participantId).first()
        # if ret is not None:
        #     ytURL = ret.ytURL
        # print(ytURL)
        
    #Passerror parameter
    return render_template('gaming/participantVideo.html', ytURL=ytURL)


@gaming_bp.route("/passive/<string:pId>", methods=['POST', 'GET'])
def passiveMode(pId):
    return render_template("gaming/passive.html")

@gaming_bp.route("/active/<string:pId>", methods=['POST', 'GET'])
def activeMode(pId):
    return render_template("gaming/active.html")


@gaming_bp.route("/testPhase", methods=['POST', 'GET'])
def testPhase():
    return render_template("gaming/testPhase.html")

@gaming_bp.route("/testPhase2", methods=['POST', 'GET'])
def testPhase2():
    pId = 'G' + str(getId())
    return render_template("gaming/testPhase2.html", pId=pId)

@gaming_bp.route("/fileUpload", methods=['POST', 'GET'])
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
            return redirect('/gaming/fileUpload')

        Id = getId()
        imageName = 'G' + str(Id) + '_' + imageName
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], imageName))

        zipFileName = 'G' + str(Id) + '_' + zipFileName
        zipFile.save(os.path.join(app.config['UPLOAD_FOLDER'], zipFileName))
        
        participantData = Gaming.query.filter_by(pId=Id).first() 

        print("participantData ->  ", participantData)

        if participantData == None:
            participantData = Gaming(pId=Id, imageName=imageName, zipFileName=zipFileName)
            db.session.add(participantData)
            db.session.commit()
        else:
            participantData.imageName = imageName
            participantData.zipFileName = zipFileName
            db.session.commit()

        print(imageName + "\t---\t" + zipFileName)
        return redirect('/gaming/selfreportQ')

    return render_template('gaming/fileUpload.html')


@gaming_bp.route("/selfreportQ", methods=['POST', 'GET'])
def selfreportQ():
    pId = 'G' + str(getId() - 1)
    return render_template("gaming/selfreportQ.html", pId=pId)

@gaming_bp.route("/thankyou")
def thankyou():
    return render_template('gaming/thankyou.html')