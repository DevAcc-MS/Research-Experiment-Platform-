from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ActivePassiveVideo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activeId = db.Column(db.String(10), unique=True)
    passiveId = db.Column(db.String(10), unique=True)
    ytURL = db.Column(db.String(100), unique=True, nullable=False)
    activeDone = db.Column(db.Boolean, default=False)
    passiveDone = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return 'id = {0}, activeId = {1}, passiveId = {2}, ytURL = {3}, activeDone = {4}, passiveDone = {5}'.format(str(self.id), self.activeId, self.passiveId, self.ytURL, self.activeDone, self.passiveDone)

    def __init__(self, activeId, passiveId, ytURL, activeDone, passiveDone):
        self.activeId = activeId
        self.passiveId = passiveId
        self.ytURL = ytURL
        self.activeDone = activeDone
        self.passiveDone = passiveDone


# (id, image, zipfile)
class Gaming(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pId = db.Column(db.Integer, unique=True)
    imageName = db.Column(db.String(300))
    zipFileName = db.Column(db.String(300))
    
    def __repr__(self):
        return 'pId = {0}, imageName = {1}, zipFileName = {2}'.format(str(self.pId), self.imageName, self.zipFileName)

    def __init__(self, pId, imageName, zipFileName):
        self.pId = pId
        self.imageName = imageName
        self.zipFileName = zipFileName

class NonGaming(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pId = db.Column(db.Integer, unique=True)
    imageName = db.Column(db.String(300))
    zipFileName = db.Column(db.String(300))
    
    def __repr__(self):
        return 'pId = {0}, imageName = {1}, zipFileName = {2}'.format(str(self.pId), self.imageName, self.zipFileName)

    def __init__(self, pId, imageName, zipFileName):
        self.pId = pId
        self.imageName = imageName
        self.zipFileName = zipFileName
    