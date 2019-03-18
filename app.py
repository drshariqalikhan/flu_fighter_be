from flask import Flask, request,jsonify,send_from_directory
# from bs4 import BeautifulSoup 
import requests
import os
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from files.newsapi import getNewsUpdates
from files.geo import getCity,getLatLon
from files.aboutflu import parseCsvFolder
from files.continent import Cont_dict
import datetime
from geopy import distance
from files.weather import getWeather
from sqlalchemy import text #for raw sql 


app = Flask(__name__)

DATABASE_DEFAULT = 'postgresql://postgres:14051976@localhost/fludb'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_DEFAULT

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
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




class SearchByUser(db.Model):
   __tablename__ = 'search_table'

   id = db.Column(db.Integer,primary_key = True)
   uid = db.Column(db.String(80))
   timestamp = db.Column(db.DateTime)
   lat = db.Column(db.Float)
   lon = db.Column(db.Float)


   def __init__(self,uid,timestamp,lat,lon):

      self.uid = uid
      self.timestamp = timestamp
      self.lat = lat
      self.lon = lon

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
   
      
@app.route('/q',methods = ['GET','POST'])
def getSearchByUsers():
   if request.method == 'GET':


      user_list =[]
      all_users = SearchByUser.query.all()
      for user in all_users:


         user_element ={
            'Uid' :f"{user.uid}",
            'Time':f"{user.timestamp}",
            'Lat':f"{user.lat}",
            'Lon':f"{user.lon}",
            }
         
         user_list.append(user_element) 
         
      return jsonify(user_list)
   if request.method == 'POST':
      rows = SearchByUser.query.delete()
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
   sendNotif("FLU FIGHTER ASIA - NEW FLU UPDATES!!")
   return "Flu done"


def sendNotif(data):
   header = {"Content-Type": "application/json; charset=utf-8","Authorization": "Basic YzM0MDBlYTktN2FmNC00OWYzLThjMDUtNDU5ZmZiNDBmOTQ4"}
   payload = {"app_id": "851420b5-ceed-445c-822e-078a4a19d9d5","included_segments": ["All"],"contents": {"en": "%s"%(data)}}
   requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))

def FluUsersNearBy(uiid,lat,lon,rad):
  
   sql = text("SELECT * FROM user_table WHERE timestamp >= CURRENT_TIMESTAMP - INTERVAL '7DAYS' AND hasflu = 'true' AND uid !="+f"'{uiid}'")
   All_other_users_in_last_7_days_with_flu = db.engine.execute(sql).fetchall()
   
   flu_user_list = []
   flu_user_uid_list = []
   # print( "ALL: %s"%All_other_users_in_last_7_days_with_flu)
   for flu_user in All_other_users_in_last_7_days_with_flu:
      #make sure no duplicate uids
      if flu_user.uid not in flu_user_uid_list:
         #add to uid list
         flu_user_uid_list.append(flu_user.uid)
         #check for unique flu uid in location
         flu_user_location = (flu_user.lat,flu_user.lon)
         uid_location = (lat,lon)
         if distance.distance(flu_user_location, uid_location).km < rad :
            flu_user_list.append(flu_user)
   # print("Unique: %s"%flu_user_list)         
   return len(flu_user_list)
     

@app.route('/f')
def OneApi():

   usersearch = request.args.get('usersearch')
   lat = request.args.get('lat')
   lon = request.args.get('lon')
   hasflu = request.args.get('hasflu')
   uid = request.args.get('uid')
   timestamp = datetime.datetime.now()
   # if its not a usersearch save to db user table
   if usersearch == 'false':
      user = User(uid,timestamp,lat,lon,hasflu)
      db.session.add(user)
      db.session.commit()
   #else save to searchByUser table   
   else:
      searchByUser = SearchByUser(uid,timestamp,lat,lon)
      db.session.add(searchByUser)
      db.session.commit()  

   user_location = getCity(lat,lon)
   country = user_location[0]
   code = user_location[1]
   # print(code)
   # l = getNewsUpdates() #comment out


   data = flunews.query.first()
   l = json.loads(str(data)) #this is a dict


   fdata = fludetail.query.first()
   d = json.loads(str(fdata)) #this is a dict
   # print(d[0]['country'])

   flu_country_data = getFluDataFrom(d,code)
   # flu_country_data = selectFluCountry(code,d)

 
   #get flu users nearby
   flu_users_nearby = FluUsersNearBy(uid,lat,lon,1)

   #get location weather 
   weather = getWeather(lat,lon)

      
   data_out = {

      'AdUnitID':'ca-app-pub-3940256099942544/6300978111',
      'country':country,
      'code':code,
      'fludata': flu_country_data,
      'news':l,
      'fluNear':flu_users_nearby,
      'weather':weather,

      }

   return jsonify(data_out)


#todo create api to get just location based fludata
@app.route('/e')
def getFluData():

   lat = request.args.get('lat')
   lon = request.args.get('lon')
   uid = request.args.get('uid')

   user_location = getCity(lat,lon)
   country = user_location[0]
   code = user_location[1]

   fdata = fludetail.query.first()
   d = json.loads(str(fdata)) #this is a dict

   flu_country_data = getFluDataFrom(d,code)
    #get location weather 
   weather = getWeather(lat,lon)

   data_out={
      'fludata': flu_country_data,
      'weather':weather,
   }

   return jsonify(data_out)


@app.route('/city')
def getCiti():


   searchTerm = request.args.get('q')
   uid = request.args.get('uid')
   timestamp = datetime.datetime.now()

   #todo save in db 
   

   out = {
      'result': getLatLon(searchTerm),
   }
   return jsonify(out)


def getFluDataFrom(myfludatalist,mylocationCode):
   result_list=[]
   #check if mylocationCode is in myfludatalist
   for myfludata in myfludatalist:
      if mylocationCode==myfludata['country']:
         #add to result_list 
         result_list.append(myfludata)
   if not result_list:
      # print('intheloop')
   #if not ,
   # update mylocationCode
      mylocationCode = getFluContienent(mylocationCode) 
      # print("loc is %s"%mylocationCode)
      # and recheck myfludatalist
      for otherfludata in myfludatalist:
         # print(otherfludata['country'])
         if mylocationCode == otherfludata['country']:
            result_list.append(otherfludata)
   return result_list

def selectFluCountry(loc_code,fludata_dict_list):
   fludata_aslist = []
   for fludata in fludata_dict_list:
      if fludata['country'] == loc_code:
         fludata_aslist.append(fludata)
         return fludata_aslist
         



def getFluContienent(loc_code):
      
   # North America xNo
   # South America xSo
   # Europe        xEu           
   # Asia          xAs  
   # Africa        xAf  
   # Australia     xAu
   # unknown       xx   

   #check loc_code against keys in Cont_dict 
   location_code = loc_code.upper()
   if location_code in Cont_dict:
      cont = Cont_dict.get(location_code)
      
      out_val = 'x'+cont[:2]
      return out_val
   else:
      return 'xx'   




if __name__ == "__main__":
    app.run()

