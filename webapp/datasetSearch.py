"""
Get the list of datasets / packages using `package_search` action and a query parameter.
The query parameter 'q' can be  a package name returned from package_list or a tag name returned from tag_list.
The function also saves the list of datasets to excel and csv.

The API url is https://data.gov.ie/api/3/action/package_search plus whatever query parameters.




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

sql = 'truncate table datasets'
cursor.execute(sql)


url = 'https://data.gov.ie/api/3/action/'
action = 'package_search' 
response = requests.get(url+action)
data = response.json()

def getDataset(url,action, params):
    #print(url+action,params)
    response = requests.get(url+'package_search',params)
    print(response.status_code)
    data=response.json()

    filename = "data.json"
            
    if filename:

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)


    for result in data["result"]["results"]:
        resources = result['resources']
        for resource in resources:
            #print(resource['package_id'], resource['name'], resource['description'], resource['url'],resource['format'],resource['created'] )
            #values = "('" + resource['package_id'] + "',)" 
            #values = eval(values)
           
           
            
            sql="insert into datasets (id, package_id, name,  description, url, format, created) values (%s,%s,%s,%s,%s,%s,%s)"
            values = [
                resource['id'],
                resource['package_id'],
                resource['name'],
                resource['description'],
                resource['url'],
                resource['format'],
                resource['created']]
            cursor.execute(sql, values)
    db.commit()
    cursor.close()

           

    


params = {'q': 'accidents' } 
getDataset('https://data.gov.ie/api/3/action/','package_search',params)

