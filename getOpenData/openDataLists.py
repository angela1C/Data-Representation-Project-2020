"""
Dec 4th
A function to pull in the lists of organisations, list of datasets / packages and list of tags.
The function can be called with 3 of the data.gov.ie API actions,
- organization_list
- package_list 
- tag_list.
The API url is https://data.gov.ie/api/3/action/ plus whatever action.
There is no query parameter required for these action calls.
The json data is downloaded to a json file based on the action call.
"""

# import the libraries
import requests
import json
import sys

# define the function, takes the base api url and the action
def  getOpenData(url, action):
    
    try:
        # create the filename based on the action name, save into the data folder
        filename = "../data/" + action + ".json"
        print(filename)
        
        # call the api and get the json data
        response = requests.get(url+action)
        data = response.json()
        #print(data)
        print("writing the returned JSON to an json file")
        if filename:
        # write the json data
            with open(filename, 'w') as f:
                # if i want just the result use data['result']
                json.dump(data, f, indent=4)
        # if the success key is not True raise system error
        if not data['success']:
            raise SystemError
        # if the result key is empty  
        if len(data['result']) == 0:
            
            return ("None found")        
    #        
    except SystemError:
        print("Bad request, please check the url and action provided.")
        sys.exit(1)
    # any other exceptions
    except Exception as e:
        print(e)
        sys.exit(1)
# call the function on the 3 list api action calls       
getOpenData('https://data.gov.ie/api/3/action/','package_list' )
getOpenData('https://data.gov.ie/api/3/action/','tag_list' )
getOpenData('https://data.gov.ie/api/3/action/','organization_list' )

