from flask import Flask, request,jsonify,send_from_directory
# from bs4 import BeautifulSoup 
import requests
import os
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from files.newsapi import getNewsUpdates
from files.geo import getCity
from files.aboutflu import parseCsvFolder
import datetime

app = Flask(__name__)

DATABASE_DEFAULT = 'postgresql://postgres:14051976@localhost/fludb'
# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_DEFAULT

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.debug = True

db = SQLAlchemy(app)

###Models

class User(db.Model):


   __tablename__ = 'user_table'

   id = db.Column(db.Integer,primary_key = True)
   uid = db.Column(db.String(80))
   timestamp = db.Column(db.DateTime)
   lat = db.Column(db.Float)
   lon = db.Column(db.Float)
   hasflu = db.Column(db.String(80))

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


#######

@app.route('/')
def index(): 
   SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
   folder_path = os.listdir(os.path.join(SITE_ROOT,'flucsv'))
   li = parseCsvFolder(folder_path,SITE_ROOT)
   return "%s"%li[0]


@app.route('/users',methods = ['GET','POST'])
def getUsers():
   if request.method == 'GET':


      user_list =[]
      all_users = User.query.all()
      for user in all_users:


         user_element ={
            'Uid' :f"{user.uid}",
            'Time':f"{user.timestamp}",
            'Lat':f"{user.lat}",
            'Lon':f"{user.lon}",
            'flu':f"{user.hasflu}"
            }
         
         user_list.append(user_element) 
         
      return jsonify(user_list)
   if request.method == 'POST':
      rows = User.query.delete()
      db.session.commit()
      return "%s deleted"%rows   
   
      




def makedb():
   db.create_all()


#API to save Flu news
@app.route('/n')
def NewsApi():


   flunews.query.delete()
   news_data = getNewsUpdates()     
   y = json.dumps(news_data) #this is a json
   mynews = flunews(y)
   db.session.add(mynews)
   db.session.commit()
   return "news done"
   


#API to save FLu Data
@app.route('/d')
def FluApi():
   
   fludetail.query.delete()
   SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
   folder_path = os.listdir(os.path.join(SITE_ROOT,'flucsv'))
   flu_data = parseCsvFolder(folder_path,SITE_ROOT)
   y = json.dumps(flu_data) #this is a json
   myflu = fludetail(y)
   db.session.add(myflu)
   db.session.commit()
   return "Flu done"

@app.route('/f')
def OneApi():

  
   lat = request.args.get('lat')
   lon = request.args.get('lon')
   hasflu = request.args.get('hasflu')
   uid = request.args.get('uid')
   timestamp = datetime.datetime.now()
   # save to db table
   user = User(uid,timestamp,lat,lon,hasflu)
   db.session.add(user)
   db.session.commit()

   user_location = getCity(lat,lon)
   country = user_location[0]
   code = user_location[1]
   # l = getNewsUpdates() #comment out

   #TODO: get l from db table

   data = flunews.query.first()
   l = json.loads(str(data)) #this is a dict

   #TODO: get d from db table

   fdata = fludetail.query.first()
   d = json.loads(str(fdata)) #this is a dict

   # SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
   # folder_path = os.listdir(os.path.join(SITE_ROOT,'flucsv'))
   # d = parseCsvFolder(folder_path,SITE_ROOT)
      
   data_out = {


      'country':country,
      'code':code,
      'fludata': d,
      'news':l,
      }

   return jsonify(data_out)




if __name__ == "__main__":
    app.run()

