import mysql.connector
from mysql.connector import cursor
import dbconfig as cfg

import requests
import json
import sys

class OpenDAO:
    # create a variable to store the database connections
    db = ""

    def __init__(self):
    # init is called when the construction function here is called.
        self.url = 'https://data.gov.ie/api/3/action/'        
        # connect to the database

        self.db = mysql.connector.connect(
            host = cfg.mysql['host'],
            user = cfg.mysql['user'],
            password = cfg.mysql['password'],
            database = cfg.mysql['db']
        )
        print("connection made")

    # clear the tables of all data
    def truncateOrgsTable(self):
        cursor = self.db.cursor()
        sql ="truncate table org_list"
        cursor.execute(sql)
        self.db.commit()
        #cursor.close()

    def truncateDatasetsTable(self):
        cursor = self.db.cursor()
        sql ="truncate table dataset_list"
        cursor.execute(sql)
        self.db.commit()
        #cursor.close()

    def truncateTagsTable(self):
        cursor = self.db.cursor()
        sql ="truncate table tag_list"
        cursor.execute(sql)
        self.db.commit()
        #cursor.close()

    def truncateDatasets(self):
        cursor = self.db.cursor()
        sql ="truncate table datasets"
        cursor.execute(sql)
        self.db.commit()
        #cursor.close()
        


    def loadOrgsTable(self, action='organization_list'):
        self.action = action
        self.response = requests.get(self.url+action)
        data = self.response.json()
        cursor = self.db.cursor()
        for result in data['result']:

            value = "('" + result + "',)" 
            sql="insert into org_list (organization) values (%s);"
    # to get it into a tuple
            values = eval(value)
            cursor.execute(sql,values)
        self.db.commit()
        cursor.close()


    def loadTagsTable(self, action='tag_list'):
        self.action = action
        self.response = requests.get(self.url+action)
        data = self.response.json()
        cursor = self.db.cursor()
        for result in data['result']:

            value = "('" + result + "',)" 
            sql="insert into tag_list (tag) values (%s);"
    # to get it into a tuple
            values = eval(value)
            cursor.execute(sql,values)
        self.db.commit()
        cursor.close()    

    def loadDatasetsTable(self, action='package_list'):
        self.action = action
        self.response = requests.get(self.url+action)
        data = self.response.json()
        cursor = self.db.cursor()
        for result in data['result']:

            value = "('" + result + "',)" 
            sql="insert into dataset_list (package_name) values (%s);"
        # to get it into a tuple
            values = eval(value)
            cursor.execute(sql,values)
        self.db.commit()
        cursor.close()    


# HERE!

   



    # I won't truncate this table. Instead use ignore insert to prevent entries with duplicate primary keys if the
    # function is called with the same query parameter

    # maybe I should not have this as the same class. Only have the API calls withe 


    query = {'q':'phone'}
    #def datasetSearch(self,action ="package_search", params={'q': 'accidents' }):
    def datasetSearch(self,action ="package_search", params=query):    
        #params= {'q': 'accidents' } 
        self.action = action
        
        self.response = requests.get(self.url+action,params)
        data = self.response.json()
        cursor = self.db.cursor()

        for result in data["result"]["results"]:
            resources = result['resources']
            for resource in resources:
            #print(resource['package_id'], resource['name'], resource['description'], resource['url'],resource['format'],resource['created'] )
            #values = "('" + resource['package_id'] + "',)" 
            #values = eval(values)
           
           
            
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




# create an instance of the object   
openDAO = OpenDAO()
