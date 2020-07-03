from bs4 import BeautifulSoup
import requests
import re
import json
import time
import os
import folium
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim,Pelias
url = "https://www.gov.sg/article/covid-19-public-places-visited-by-cases-in-the-community-during-infectious-period"
# "https://www.gov.sg/article/covid-19-public-places-visited-by-cases-in-the-community-during-infectious-period"



def getCovidList():
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    geolocator = Nominatim(user_agent="sg_safe_entry_plus")
    # geolocator = Pelias(domain = 'http://speromedtech.com/',user_agent="sg_safe_entry_plus")


    data = []
    table = soup.find('table', attrs={'class':'table'})
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')

        cols = [ele.text.strip() for ele in cols]
            
        l = cols[2].replace('\n',' ')
        try:
            q = re.search('\(([^)]+)', l).group(1)

        except:
            try:
                q=re.search('(\d+\w+ \w+ \w+ \w+)',l).group(1)
            except:
                pass
            # q = "963 Jurong West Street 91"  
        # print(f'q value :  {q}')
        
        try:
            cloc_lat,cloc_lon,cloc_alt =  geolocator.geocode(f"{q},Singapore").point

            data.append(
                {
                    'date':cols[0],
                    'time':cols[1],
                    'place':cols[2].replace('\n',' '),
                    'lat' : cloc_lat,
                    'lon' : cloc_lon
                    # 'lat':(geolocator.geocode(query = 'f"{q},Singapore"')).latitude,
                    # 'lon':(geolocator.geocode(query = 'f"{q},Singapore"')).longitude,
                    # 'lat':(geolocator.geocode(f"{q},Singapore")).latitude,
                    # 'lon':(geolocator.geocode(f"{q},Singapore")).longitude,
                })
        except:
            data.append(
                {
                    'date':cols[0],
                    'time':cols[1],
                    'place':cols[2].replace('\n',' '),
                    'lat':None,
                    'lon':None,
                })
            print(f'error in adding data {cols[0]}')
            pass    

    return (data,len(data))

# x,y = getCovidList()
# out = {
#     'D':x,
#     'N':y
# }

# print(out)

# print(x)
# print(y)


# def getPlaces(site_root):

#     CovfilePath = os.path.join(site_root,'cdata','covid.txt')
#     # CovfilePath = ('\\Users\\drsha\\Documents\\mycode\\flu_fighter_be\\cdata\\covid.txt')
#     #get getStoredPlaces() as Placeslist
#     with open(CovfilePath) as json_file:
#         data = json.load(json_file)
#         uploadTime = data['TimeUpdated']
#         currentTime = time.time()
#         print(f'old {uploadTime} and now {currentTime}')

#         #compare times
#         if currentTime - uploadTime > 45000:
#             #scrape page and update covid.txt data and updatetime
#             newData,newN = getCovidList()
#             updatedData ={
#                 "Data":newData,
#                 "TimeUpdated":currentTime,
#                 "Num":newN
#             }
#             with open(CovfilePath,'w') as outfile:
#                 json.dump(updatedData,outfile)

#             #return scarped data only 
#             return (updatedData['Data'],updatedData['Num'])
#         else:
#             #return data
#             return (data['Data'],data['Num'])


# x,y = getPlaces(os.path.realpath(os.path.dirname(__file__)))

# print(x)


#map.html
def displayCovidMap():
    #Define coordinates of where we want to center our map
    base_coords = [1.3521, 103.8198]
    covData, num = getCovidList()

    
    #Create the map
    my_map = folium.Map(location = base_coords, zoom_start = 13)

    #add markers to map
    for covdat in covData:
        if covdat['lat'] != None:
            locdat = [covdat['lat'],covdat['lon']]
            locDetails = f"{covdat['place']} \n {covdat['date']}"
            #add marker
            folium.Marker(locdat, popup = locDetails).add_to(my_map)
        else:
            pass

    #Display the map
    return my_map._repr_html_()



