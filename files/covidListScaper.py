from bs4 import BeautifulSoup
import requests
import re
from geopy.geocoders import Nominatim
url = "https://www.gov.sg/article/covid-19-public-places-visited-by-cases-in-the-community-during-infectious-period"

# req = requests.get(main_url)
# soup = BeautifulSoup(req.text, "html.parser")
# geolocator = Nominatim(user_agent="sg_safe_entry_plus")


# data = []
# table = soup.find('table', attrs={'class':'table'})
# table_body = table.find('tbody')

# rows = table_body.find_all('tr')
# for row in rows:
#     cols = row.find_all('td')

#     cols = [ele.text.strip() for ele in cols]
        
#     l = cols[2].replace('\n',' ')
#     try:
#         q = re.search('\(([^)]+)', l).group(1)

#     except:
#         try:
#             q=re.search('(\d+\w+ \w+ \w+ \w+)',l).group(1)
#         except:
#             pass
#         # q = "963 Jurong West Street 91"  
#     # print(q)
    
    
#     try:
#         data.append(
#             {
#                 'date':cols[0],'time':cols[1],
#                 'place':cols[2].replace('\n',' '),
#                 'lat':(geolocator.geocode(f"{q},Singapore")).latitude,
#                 'lon':(geolocator.geocode(f"{q},Singapore")).longitude,
#             })
#     except:
#         pass    

# print(data)


def getCovidList():
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    geolocator = Nominatim(user_agent="sg_safe_entry_plus")


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
        # print(q)
        
        try:
            data.append(
                {
                    'date':cols[0],
                    'time':cols[1],
                    'place':cols[2].replace('\n',' '),
                    'lat':(geolocator.geocode(f"{q},Singapore")).latitude,
                    'lon':(geolocator.geocode(f"{q},Singapore")).longitude,
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
            print('err')
            pass    

    return (data,len(data))

# x,y = getCovidList(main_url)
# print(x)
# print(y)
