import mysql.connector
from mysql.connector import cursor
import dbconfig as cfg

import requests
import json
import sys


class SearchDAO:
    # create a variable to store the database connections
    db = ""

    def __init__(self):
    # init is called when the construction function here is called.
        self.url = 'https://data.gov.ie/api/3/action/'  
        self.action=  "package_search"  
        self.params = "?q=" 
        #self.params = params
        # connect to the database

        self.db = mysql.connector.connect(
            host = cfg.mysql['host'],
            user = cfg.mysql['user'],
            password = cfg.mysql['password'],
            database = cfg.mysql['db']
        )
        print("connection made")
    
    
    #def datasetSearch(self,action ="package_search", params={'q': 'accidents' }):
    
    def datasetSearch(self, params):   
        self.params= self.params+params
        
        
        self.response = requests.get(self.url+self.action+self.params)
        print(self.response)
        data = self.response.json()
        cursor = self.db.cursor()

        for result in data["result"]["results"]:
            resources = result['resources']
            for resource in resources:
                print(resource['name'])
                sql="insert ignore into datasets (id, package_id, name,  description, url, format, created) values (%s,%s,%s,%s,%s,%s,%s)"
                values = [
                    resource['id'],
                    resource['package_id'],
                    resource['name'],
                    resource['description'],
                    resource['url'],
                    resource['format'],
                    resource['created']]
                cursor.execute(sql, values)
        self.db.commit()
        cursor.close()

    def delete(self,id):
        cursor = self.db.cursor()
        sql="delete from datasets where id= %s"
        values = (id,)
        cursor.execute(sql, values)
        self.db.commit()
        cursor.close()

# create an instance of the object   
searchDAO = SearchDAO()

# https://data.gov.ie/api/3/action/package_search