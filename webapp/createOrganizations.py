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

############## ORGANIZATIONS

sql = 'truncate table org_list'
cursor.execute(sql)


url = 'https://data.gov.ie/api/3/action/'
action = 'organization_list' 
response = requests.get(url+action)
data = response.json()

for result in data['result']:

    value = "('" + result + "',)" 
    sql="insert into org_list (organization) values (%s);"
    # to get it into a tuple

    values = eval(value)
    cursor.execute(sql,values)
    #print(org)

db.commit()
cursor.close()
