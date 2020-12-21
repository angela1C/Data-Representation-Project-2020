"""
In addition to the url, provide the query parameter in a dictionary with the `id` key and value 
 being the tag name returned from call to 'https://data.gov.ie/api/3/action/organization_list'

organization_show just seems to return some details of users at the organisation. 

See openDataShow.py for this in a function
"""



import requests
import json
from xlwt import *

url = "https://data.gov.ie/api/3/action/"
action = "organization_show"
params = {'id': 'central-bank-of-ireland'}
URL_API = url + action
response = requests.get(URL_API,params)
#response = requests.get("https://data.gov.ie/api/3/action/tag_show?id=atmospheric conditions and meteorological geographical features")
data = response.json()


print(response.status_code)
data = response.json()
#print(data)

print("writing the returned JSON to an json file")
filename = params['id'] + ".json"
if filename:
    # write the json data
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)