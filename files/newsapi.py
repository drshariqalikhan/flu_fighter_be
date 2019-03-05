import requests
import json


def getNewsUpdates():

   all_article_List =[]
   for x in range(2):
      url = "https://newsapi.org/v2/everything?apiKey=f8099a1195b644778418d27ede3071f9&q=flu OR influenza &pageSize=100&sortBy=relevancy&page=%s"%x
      r= requests.get(url)
      json_data = json.loads(r.text)

      try:

         article_List = json_data.get("articles")
         for article in article_List:
            title = article.get('title')
            descrip = article.get('description')
            article_url = article.get('url')
            imageurl = article.get('urlToImage')
            source = article.get('source').get('name')
            article_date = article.get('publishedAt')
            data = {

               'title':title,
               'descrip':descrip,
               'article_url':article_url,
               'imageurl':imageurl,
               'source':source,
               'article_date':article_date

               }
            all_article_List.append(data)
      except:

         pass
   return all_article_List