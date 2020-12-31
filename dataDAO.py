import mysql.connector
from mysql.connector import cursor
import dbconfig as cfg

import requests
import json
import sys

class DataDAO:


    def initConnectToDB(self):
        db = mysql.connector.connect(
            host=       cfg.mysql['host'],
            user=       cfg.mysql['user'],
            password=   cfg.mysql['password'],
            database=   cfg.mysql['db'],
            pool_name='my_connection_pool',
            pool_size=20
        )
        return db

    def getConnection(self):
        db = mysql.connector.connect(
            pool_name='my_connection_pool'
        )
        return db

    def __init__(self): 
        db=self.initConnectToDB()
        db.close()
        print("connection made")

##   *************************** DATASET_LIST table
    # @app.route('/datasets/')
    def getAllDatasetNames(self):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql =  'select * from dataset_list;'
        cursor.execute(sql,)
        # returns tuples, need to convert into dict objects for json later on
        results = cursor.fetchall()
        returnArray = []
        #print(results)
        for result in results:
            returnArray.append(result) 
          
        cursor.close()  
        return returnArray  

    # @app.route('/datasets/<string:query>')  
    def findDatasetByName(self, query):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql = "select * from dataset_list where package_name like %s"
            # 
        values = (query +"%",) 
            # convert to a tuple 
        values = tuple(values,)
            
        cursor.execute(sql, values)
        results = cursor.fetchall()
        returnArray = []
        for result in results:
            returnArray.append(result)            
            
        cursor.close()
        #print(returnArray)
        return returnArray


    # @app.route('/datasets/<int:id>')
    def findDatasetById(self, id):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql = "select * from dataset_list where id = %s"
        values = (id,)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        
        cursor.close()
        return result    

    # @app.route('/tags')   # TAG_LIST table
    def getAllTags(self):
        db = self.getConnection()
        cursor = db.cursor()
        sql =  'select * from tag_list;'
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        #print(results)
            # returns tuples, need to convert into dict objects for json later on
        for result in results:
            returnArray.append(self.convertToDictionaryT(result))   
        cursor.close()  
        return returnArray 

    # @app.route('/tags/<int:id>')  # TAG_LIST table
    def findTagById(self, id):
        db = self.getConnection()
        cursor = db.cursor()
        sql = "select * from tag_list where tag_id = %s"
        values = (id,)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        tag = self.convertToDictionaryT(result)
        cursor.close()
        return tag

    # @app.route('/tags/<string:char>')  # TAG_LIST table
    def findTagByChar(self, char):
        db = self.getConnection()
        cursor = db.cursor()
        sql="select * from tag_list where tag like %s;"
        values = (char,)
        cursor.execute(sql, values)
        results = cursor.fetchall()
        returnArray = []
        for result in results:
            returnArray.append(self.convertToDictionaryT(result))
        
        cursor.close()
        return returnArray

    def convertToDictionaryT(self, result):
            colnames=['id','tag_name']
            item = {}
            
            if result:
                for i, colName in enumerate(colnames):
                    value = result[i]
                    item[colName] = value
            
            return item

    # @app.route('/orgs')  # ORG_LIST table
    def getAllOrgs(self):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql =  'select * from org_list;'
        cursor.execute(sql)
            # returns tuples, need to convert into dict objects for json later on
        results = cursor.fetchall()
        returnArray = []
            #print(results)
        for result in results:
            returnArray.append(result)   
        cursor.close()  
        return returnArray 

    # @app.route('/orgs/<int:id>')  # ORG_LIST table
    def findOrgById(self, id):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql = "select * from org_list where org_id = %s"
        values = (id,)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        cursor.close()
        return result

    # @app.route('/orgs/<string:query>') # ORG_LIST table
    def findOrgs(self, query):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql = "select * from org_list where organization like %s"
            # 
        values = (query +"%",) 
            # convert to a tuple 
        values = tuple(values,)
            
        cursor.execute(sql, values)
        results = cursor.fetchall()
        returnArray = []
        for result in results:
            returnArray.append(result)            
            
        cursor.close()
        #print(returnArray)
        return returnArray



    def convertToDictionaryDS(self, result):
            colnames=['id','package_id','name','description','url','format','created']
            item = {}
            
            if result:
                for i, colName in enumerate(colnames):
                    value = result[i]
                    item[colName] = value
            
            return item

### *************************  CRUD on DATASETS TABLE    *************************************************            
# this is separate table to the list of datasets, this is populated from the package_search api call to data.gov.ie
# see searchDAO file

    # @app.route ('/dataset_resources)
    def getAllResources(self):
        db = self.getConnection()
        # https://stackoverflow.com/questions/43796423/python-converting-mysql-query-result-to-json
        cursor = db.cursor(dictionary=True)
        sql = "select * from datasets"
    
        #sql = "select * from datasets"
        cursor.execute(sql,)
        results = cursor.fetchall()
        returnArray = []
        for result in results:
            returnArray.append(result)   
        cursor.close()  
        return returnArray 

    # @app.route('/dataset_resources/<string:id>')
    # 
    def findResourceById(self,id):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql = "select * from datasets where id= %s"
        values = (id,)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        cursor.close()
        #print(result)
        
        return result

    # @app.route('/queryresources/<string:query>')
    def findADataset(self, query):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql = "select * from datasets where name like %s"
        # 
        values = (query +"%",) 
        # convert to a tuple 
        values = tuple(values,)
        print(f"the values {values}")
        cursor.execute(sql, values)
        result = cursor.fetchone()
                   
        cursor.close()

        return result


          # @app.route('/dataset_resources_query/<string:query>')
    def findDatasets(self, query):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql = "select * from datasets where name like %s"
        # 
        values = (query +"%",) 
        # convert to a tuple 
        values = tuple(values,)
        print(f"the values {values}")
        cursor.execute(sql, values)
        results = cursor.fetchall()
        
        returnArray = []
        
        for result in results:
            returnArray.append(result)            
        
        cursor.close()
        #print(returnArray)
        return returnArray


    # @app.route('/deleteresources/<string:id>', methods=['DELETE'])
    def deleteResource(self, id):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql = "delete from datasets where id= %s" 
        values = (id,)
        cursor.execute(sql, values)

        db.commit()
        print("delete done")
        cursor.close()

    # want to update a row in the table
    def updateResource(self,values):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql = "update datasets set description =%s where id = %s"
        #values=("testing update from python",id,)
        cursor.execute(sql, values)
        db.commit()
        print("update done")
        cursor.close()


        # @app.route('/datasetUrls')
    def getDatasetUrls(self):
        db = self.getConnection()
        # https://stackoverflow.com/questions/43796423/python-converting-mysql-query-result-to-json
        cursor = db.cursor(dictionary=True)
        sql = "select * from datasets where format in ('csv','json')"
        cursor.execute(sql,)
        
        results = cursor.fetchall()
        returnArray = []
        for result in results:
            returnArray.append(result)   
        cursor.close()  
        return returnArray 




      








    def addDataset(self):
        db = self.getConnection()
        cursor = db.cursor()
        sql = "insert into mydatasets (dataset) values ('testingfrompython')"
            
            #values="testing_insertfrompython";
            #print(values)
        cursor.execute(sql)
            
        self.db.commit()
        lastRowId=cursor.lastrowid
        cursor.close
        return lastRowId
        





# create an instance of the object   
dataDAO = DataDAO()

"""
    def findById(self, id):
        cursor=self.db.cursor()
        sql = "SELECT * from packages where id = %s"
        
        values = [ id ]
        cursor.execute(sql, values)
        result = cursor.fetchone()
        return result
        cursor.close() 
        #return self.convertToDict(result)

    def update(self, values):

        cursor = self.db.cursor()
        # need to use the correct order for the values
        sql = "update packages set package = %s where id = %s"
        
        cursor.execute(sql, values)
        self.db.commit()
        

    def delete(self, id):
        cursor = self.db.cursor()
        sql = "delete from packages where id = %s"
        values = (id,)
        cursor.execute(sql, values)
        self.db.commit()
        print("delete done")
"""
   