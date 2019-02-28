from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from app import db

class User(db.Model):

    __tablename__ = 'user_table'

    id = db.Column(db.Integer,primary_key = True)
    uid = db.Column(db.String(80),unique = True)
    timestamp = db.Column(db.DateTime)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    hasflu = db.Column(db.Boolean)

    def __init__(self,uid,timestamp,lat,lon,hasflu):
        self.uid = uid
        self.timestamp = timestamp
        self.lat = lat
        self.lon = lon
        self.hasflu = hasflu

    def __repr__(self):
        return '<uid %r>' %self.uid

class flunews(db.Model):

    __tablename__ = 'news'

    id = db.Column(db.Integer,primary_key = True)
    newsjson = db.Column(db.JSON)

    def __init__(self,newsjson):
        self.newsjson = newsjson

    def __repr__(self):
        # return '%r' %self.
        return self.newsjson

class fludetail(db.Model):
    __tablename__ = 'fludeatil'

    id = db.Column(db.Integer,primary_key = True)
    flujson = db.Column(db.JSON)

    def __init__(self,flujson):
        self.flujson = flujson

    def __repr__(self):
        return self.flujson


db.create_all()