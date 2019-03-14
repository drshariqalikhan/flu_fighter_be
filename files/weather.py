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
    # weather_list = []

    outer_list = []
    
    if 'list' in json_data_w:
        weather_list = json_data_w['list']
        
        for weather_element in weather_list:
            data_list = []    
            if 'temp' in weather_element['main']:
                data_list.append(weather_element['main']['temp'])
            else:
                data_list.append(999)
            if 'main' in weather_element['weather'][0]:
                data_list.append(weather_element['weather'][0]['main'])
            else:
                data_list.append('999')
            if 'icon' in weather_element['weather'][0]:
                data_list.append(weather_element['weather'][0]['icon'])
            else:
                data_list.append('10n')    
            if 'dt' in weather_element:
                data_list.append(weather_element['dt'])
            else:
                data_list.append(999)
            dict = {
                'temp':data_list[0],
                'main':data_list[1],
                'icon':data_list[2],
                'dt':data_list[3]
            }
            outer_list.append(dict)









    #get citydata
    
    country ='unknown'
    name ='unknown'

    if 'country' in json_data_w['city']:
        country = json_data_w['city']['country']
    if 'name' in  json_data_w['city']:
        name = json_data_w['city']['name']
    
    city ={
        'name':name,
        'country':country
    }

    # get nowdata

    weather_desc = ''
    icon = ''
    temp = 999
    humidity = 999
    temp_min = 999
    temp_max = 999
    wind_speed = 999
    sunrise  = 999
    sunset = 999

    if 'main' in json_data_n['weather'][0]:
        weather_desc = json_data_n['weather'][0]['main']
    if  'icon' in  json_data_n['weather'][0]:
        icon = json_data_n['weather']['icon']  

    if 'temp' in json_data_n['main']:
        temp = json_data_n['main']['temp']
    if 'humidity' in json_data_n['main']:
        humidity = json_data_n['main']['humidity']
    if 'temp_min' in json_data_n['main']:
        temp_min = json_data_n['main']['temp_min']        
    if 'temp_max' in json_data_n['main']:
        temp_max = json_data_n['main']['temp_max']

    if 'speed' in json_data_n['wind']:
        wind_speed = json_data_n['wind']['speed']    

    if 'sunrise' in json_data_n['sys']:
        sunrise = json_data_n['sys']['sunrise']   
    if 'sunset' in json_data_n['sys']:
        sunset = json_data_n['sys']['sunset']   


    now = {
        'weather_desc': weather_desc,
        'icon':icon,
        'temp':temp,
        'humidity':humidity,
        'temp_min':temp_min,
        'temp_max':temp_max,
        'wind_speed':wind_speed,
        'sunrise':sunrise,
        'sunset':sunset
    }        

    #get airquality
    air_quality_dict = json_data_q['data']['iaqi']

    co=999
    o3=999
    pm10=999
    pm25=999
    so2=999

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
        'forecast_list':outer_list,
        'now':now,
        'city':city,
        'air_quality_now':airq
    }
    return weatherData
