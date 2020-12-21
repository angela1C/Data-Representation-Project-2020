"""

Get the list of datasets / resources using the resource_search api action. From this get the url to the actual dataset.

Packages refer to datasets, resources contain the url of the dataset.

In addition to the url, provide the query parameter in a dictionary with the `query` key and value 
 being a tag name. I think it also takes a package id using the 'id' key instead of the 'name' key
This one is a bit different to the other api calls as I couldn't pull out the query parameter in the same way using a tag name.

Be careful writing to csv file as some tags (such as rainfall) will have a huge number of datasets.
Therefore I set a limit in the number of rows written to a csv file.

https://data.gov.ie/api/3/action/package_search?q=atmospheric conditions and meteorological geographical features
https://data.gov.ie/api/3/action/resource_search?query=name:The%20Walled%20Towns%20of%20Ireland

come back to this 
"""
import requests
import json
import csv
import sys

def getResource(url,action, params):

    try:
        # for now include the action in the url #URL = (url + action + "?query=name:"+ params['query'])
        response = requests.get(url + action + "?query=name:"+ params['query'])
        print(response.status_code)
        data = response.json()
    
        if not data['success']:
            raise SystemError

        if len(data['result']) == 0:
            raise Exception
            
        else:
            print(data['result']['count'])
            
            filename = params['query'] + ".csv"

        # create a list to hold the url and the name 
            url_list =[]
            for result in data['result']['results']:
            #print(result['url'])
                url_list.append(result['url'])
                url_list.append(result['name'])
            #print(url_list)
 
    # a csv file to write to
        with open (filename, mode ='w', newline='') as csvfile:
            # 
            datawriter = csv.writer(csvfile, delimiter ='"')
            items = len(url_list)
            # limiting the number of rows to write to a csv file to prevent huge files being written
            if items < 100:
                # setting the row headers
                # writerow only takes one argument, I want to have 2 items on each row
                firstrow = ("Url",',', "Name")
                datawriter.writerow(firstrow)
                rowcount = 0
                # 
                for i in range(len(url_list)//2):
                    # creating a row
                    row = [url_list[rowcount],',',url_list[rowcount+1]]
                    datawriter.writerow(row)
                    # increment row count by 2
                    rowcount = rowcount +2;
        

            else:
                firstrow = ("Url",',', "Name")
                datawriter.writerow(firstrow)
                
                    
                rowcount = 0
                for i in range(100):
                # creating a row
                    row = [url_list[rowcount],',',url_list[rowcount+1]]
                    datawriter.writerow(row)
                    # increment row count by 2
                    rowcount = rowcount +2;                    

        print(f"writing to csv file{filename}")
            
    except SystemError:
        print("Failed request. Please check your query parameters")
        sys.exit(1)
        
    except Exception as e:
        print(e)
        sys.exit(1)

params = {'query': 'accidents'}  


myDataset = getResource('https://data.gov.ie/api/3/action/', "resource_search" ,params)

