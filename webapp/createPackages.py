"""
I needed to convert the result into the right format to get it into the sql
needs to be a list or a tuple.
"""


import requests
import json
import sys
import mysql.connector
import dbconfig as cfg


db = mysql.connector.connect(
    host = cfg.mysql['host'],
    user = cfg.mysql['user'],
    password = cfg.mysql['password'],
    database = cfg.mysql['db']
    
)
cursor = db.cursor()

      
# first clear the table so I am not entering twice

sql = 'truncate table dataset_list'
cursor.execute(sql)


url = 'https://data.gov.ie/api/3/action/'
action = 'package_list' 
response = requests.get(url+action)
data = response.json()

for result in data['result']:

    value = "('" + result + "',)" 
    sql="insert into dataset_list (package_name) values (%s);"
    # to get it into a tuple

    values = eval(value)
    cursor.execute(sql,values)
    #print(org)

db.commit()
cursor.close()



sql = 'truncate table tag_list'
cursor.execute(sql)


url = 'https://data.gov.ie/api/3/action/'
action = 'tag_list' 
response = requests.get(url+action)
data = response.json()

for result in data['result']:

    value = "('" + result + "',)" 
    sql="insert into tag_list (tag) values (%s);"
    # to get it into a tuple

    values = eval(value)
    cursor.execute(sql,values)
    #print(org)

db.commit()
cursor.close()
