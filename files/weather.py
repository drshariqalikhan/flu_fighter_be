import requests
import json
from collections import defaultdict
import time

def getWeather(lat,lon):
    n_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=bed628740ac3ce2655a4dd92e21b1c73&cnt=8&units=metric'
    w_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid=bed628740ac3ce2655a4dd92e21b1c73&cnt=8&units=metric"
    q_url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token=ec80cc948e41a99f27d09e14b31d96bfdd93262e"
    rn= requests.get(n_url)
    rw= requests.get(w_url)
    rq = requests.get(q_url)
    json_data_n = json.loads(rn.text)
    json_data_w = json.loads(rw.text)
    json_data_q = json.loads(rq.text)

    #get (8) 3hrly weather data
    weather_list = json_data_w['list']
    city = json_data_w['city']
    
    #get airquality
    air_quality_dict = json_data_q['data']['iaqi']

    co=''
    o3=''
    pm10=''
    pm25=''
    so2=''

    if 'co' in air_quality_dict:
        co = air_quality_dict['co']['v']
    if 'o3' in air_quality_dict:
        o3 = air_quality_dict['o3']['v']
    if 'pm10' in air_quality_dict:
        pm10 = air_quality_dict['pm10']['v']
    if 'pm25' in air_quality_dict:
        pm25 = air_quality_dict['pm25']['v']
    if 'so2' in air_quality_dict:
        so2 = air_quality_dict['so2']['v']        

    airq = {
        'co':co,
        'o3':o3,
        'pm10':pm10,
        'pm25':pm25,
        'so2':so2,
        

    }
    airq = defaultdict(lambda: -1, airq)



    weatherData= {
        'forecast_list':weather_list,
        'now':json_data_n,
        'city':city,
        'air_quality_now':airq
    }
    return weatherData
