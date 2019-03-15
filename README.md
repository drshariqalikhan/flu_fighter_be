back end for flu fighter asia

steps to create and deploy on heroku
1. create virtual env using virtualenv name
2. install flask,sqlalchemy,psycopg2,gunicorn
3. create procfile, requirements.txt
4. pip freeze > requirements.txt
5. make flask apis, add sqlalchemy connection string 
6. create postgresql table
6a. make new model class -> run python -c "import app; app.makedb()" 
7. git init
8. add to git repo
9. create heroku app with heroku create
10. add heroku postgres 
11. connect heroku to github
12. git push heroku master
13. heroku run python nameofdbcreationfunc()
 