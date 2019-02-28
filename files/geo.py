from geopy.geocoders import Nominatim

def getCity(lat,lon):
    dat = []
    try:
        geolocator = Nominatim(user_agent="specify_your_app_name_here")
        location = geolocator.reverse("%s , %s"%(lat,lon))
        data = location.raw
        country = data.get('address').get('country')
        country_code = data.get('address').get('country_code')
        dat.append(country)
        dat.append(country_code)
    except:
        pass
    return dat
