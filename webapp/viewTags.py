"""
View tags
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

 


sql="select * from tag_list where tag like %s;"
    # to get it into a tuple
# % represents 0,1 or multiple characters
# _ represents a single character

values = ('F%',)
#cursor.execute(sql,values)
cursor.execute(sql,values)
result = cursor.fetchall()

for x in result:
    print(x)
