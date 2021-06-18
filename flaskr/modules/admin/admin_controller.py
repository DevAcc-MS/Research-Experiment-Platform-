from flask import render_template, redirect
from flask.globals import request
from . import admin_bp
from flaskr.models import ActivePassiveVideo, db

@admin_bp.route("/")
def login():
    return render_template('admin/admin.html')


@admin_bp.route("/participantList", methods= ['POST', 'GET'])
def participantList():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        print (username, password)
        if username == 'cogsci' and password == 'cogsci123':
            allData = ActivePassiveVideo.query.all()
            return render_template('admin/participantList.html', data=allData)
    return render_template('admin/admin.html')

@admin_bp.route("/updateParticipantView", methods=['POST', 'GET'])
def updateParticipantView():
    if request.method == 'POST':
        activeId = request.form.get('activeId')
        dataRow = ActivePassiveVideo.query.filter_by(activeId=activeId).first()
        return render_template('admin/updateParticipant.html', data=dataRow)
    return render_template('admin/admin.html')

@admin_bp.route("/updateParticipant", methods=['POST', 'GET'])
def updateParticipant():
    activeId = request.form.get('activeId')
    passiveId = request.form.get('passiveId')
    ytURL = request.form.get('ytURL')
    
    dataRow = ActivePassiveVideo.query.filter_by(activeId=activeId).first()
    dataRow.passiveId = passiveId
    dataRow.ytURL = ytURL
    db.session.commit()

    allData = ActivePassiveVideo.query.all()
    return render_template('admin/participantList.html', data=allData)

@admin_bp.route("/addRecord", methods=['POST', 'GET'])
def addRecord():
    if request.method == 'POST':
        activeId = request.form.get('activeId')
        passiveId = request.form.get('passiveId')
        ytURL = request.form.get('ytURL')
        activeDone = False
        passiveDone = False

        newRecord = ActivePassiveVideo(activeId, passiveId, ytURL, activeDone, passiveDone)
        db.session.add(newRecord)
        db.session.commit()
        return redirect('/admin/participantList')
    return render_template('admin/addRecord.html')
