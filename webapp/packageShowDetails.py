"""
Dec 4th
A function using the package_show action api.

The package_show action is used to get a full JSON representation of a dataset, resource or other object.

The API url is https://data.gov.ie/api/3/action/package_show plus whatever query parameters. 
The query parameter `id` can take a package name returned from the call to the package_list api 
or a package_id returned from package_search api action call.

`data.gov.ie/api/3/action/package_show?id=the-walled-towns-of-ireland`
`data.gov.ie/api/3/action/package_show?id=48b17bf2-b41d-45c1-89f8-c7ce67f7c8e0`
"""
import requests
import json
import sys

def packageShow(url, param): 
    
    try:
        # for now include the action in the url
        response = requests.get(url+'package_show',params)
        print(response.status_code)
        data = response.json()
    
        if not data['success']:
            raise SystemError

        if len(data['result']) == 0:
            raise Exception

        else:
           
            print("writing the returned JSON to an json file")
            filename = params['id'] + ".json"
            
            if filename:
            # write the json data
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=4)

            # just to see what keys are in the dictionary
            print("The json file contains the following fields:")
            resultkeys = data['result'].keys()
            print(resultkeys)
            

    except SystemError:
        print("Failed request. Please check your query parameters")
        sys.exit(1)
        
    except Exception as e:
        print(e)
        sys.exit(1)
        

#params = {'id': "014-interval-in-years-since-last-birth-total-births-live-births-mortality-rates-and-matern-2014" } 
# id can be a package name returned from package_list  
params = {'id': "2008-to-december-2009-by-licensing-authority-engine-capacity-cc-motor-cycle-make-month-and-statistic"}
# id can be package_id returned from package_search
params = {"id": "500e95c5-8ebb-4d0b-9214-74bc1530fd0c"}
myDataset = packageShow('https://data.gov.ie/api/3/action/', params)

#https://data.gov.ie/api/3/action/package_show?id=85c681c0-d410-4635-a00d-d8dc63fb72ae
