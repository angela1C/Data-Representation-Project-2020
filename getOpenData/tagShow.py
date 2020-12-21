"""
A function using the tag_show action api.
The tag_show action is used to get a full JSON representation of a dataset, resource or other object.
I don't think this is very useful. 

The API url is https://data.gov.ie/api/3/action/tag_show plus whatever query parameters.

"""
import requests
import json
import sys

def tagShow(url, param): # Action
    
    try:
        # for now include the actionin the url
        response = requests.get(url+'tag_show',params)
        print(response.status_code)
        data = response.json()
    
        if not data['success']:
            raise SystemError

        if len(data['result']) == 0:
            raise Exception

        else:
           
            print("writing the returned JSON to an json file")

            filename = "../data/" + params['id'] + ".json"
            
            if filename:
            # write the json data
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=4)
             

    except SystemError:
        print("Failed request. Please check your query parameters")
        sys.exit(1)
        
    except Exception as e:
        print(e)
        sys.exit(1)
        

params = {'id':   "2008" }     
myDataset = tagShow('https://data.gov.ie/api/3/action/', params)

