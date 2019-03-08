import requests
import json



def getWeather(lat,lon):

    w_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid=bed628740ac3ce2655a4dd92e21b1c73&cnt=8&units=metric"
    q_url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token=ec80cc948e41a99f27d09e14b31d96bfdd93262e"
    rw= requests.get(w_url)
    rq = requests.get(q_url)
    json_data_w = json.loads(rw.text)
    json_data_q = json.loads(rq.text)

    #get (8) 3hrly weather data
    weather_list = json_data_w['list']
    
    #get airquality
    air_quality_dict = json_data_q['data']['iaqi']



    weatherData= {
        'forecast_list':weather_list[1:],
        'now':weather_list[0],
        'air_quality_now':air_quality_dict
    }
    return weatherData
