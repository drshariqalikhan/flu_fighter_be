from flask import Flask, request,jsonify,send_from_directory
# from bs4 import BeautifulSoup 
import requests
import os
import json
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.dialects.postgresql import JSON
from files.newsapi import getNewsUpdates
from files.geo import getCity
from files.aboutflu import parseCsvFolder
import datetime

app = Flask(__name__)

DATABASE_DEFAULT = 'postgresql://postgres:14051976@localhost/fludb'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_DEFAULT

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.debug = True
db = SQLAlchemy(app)

@app.route('/')
def index():

    
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    folder_path = os.listdir(os.path.join(SITE_ROOT,'flucsv'))
    li = parseCsvFolder(folder_path,SITE_ROOT)
    return "%s"%li[0]


#API to save Flu news
@app.route('/n')
def NewsApi():
   pass
   


#API to save FLu Data
@app.route('/d')
def FluApi():
   pass
   

@app.route('/f')
def OneApi():

  
   lat = request.args.get('lat')
   lon = request.args.get('lon')
   hasflu = request.args.get('hasflu')
   uid = request.args.get('uid')
   timestamp = datetime.datetime.now()
   #   save to db table
#    User.query.delete()
#    user = User(uid,timestamp,lat,lon,hasflu)
#    db.session.add(user)
#    db.session.commit()

   user_location = getCity(lat,lon)
   country = user_location[0]
   code = user_location[1]
   l = getNewsUpdates() #comment out

   #TODO: get l from db table

#    data = flunews.query.first()
#    l = json.loads(str(data)) #this is a dict

   #TODO: get d from db table

   SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
   folder_path = os.listdir(os.path.join(SITE_ROOT,'flucsv'))
   d = parseCsvFolder(folder_path,SITE_ROOT)
      
   data_out = {


      'country':country,
      'code':code,
      'fludata': d,
      'news':l,
      }

   return jsonify(data_out)




if __name__ == "__main__":
    app.run()

