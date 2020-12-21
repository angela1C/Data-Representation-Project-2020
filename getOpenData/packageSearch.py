"""
Nov 25th
Get the list of packages using the package_list api action.
Save to a json file.
packages refer to datasets

 In addition to the url, provide the query parameter in a dictionary with the `id` key and value 
 being the tag name returned from call to 'https://data.gov.ie/api/3/action/package_search'

 "all-persons-aged-15-and-over-by-sex-year-and-statistic"
 https://data.gov.ie/api/3/action/package_search?q=museum
"""



import requests
import json
from xlwt import *

url = "https://data.gov.ie/api/3/action/"
action = "package_search"
q = {'q': 'museum'}
URL_API = url + action
response = requests.get(URL_API,q)
response = requests.get("https://data.gov.ie/api/3/action/package_search?q=atmospheric conditions and meteorological geographical features")
data = response.json()


print(response.status_code)
data = response.json()
#print(data)

print("writing the returned JSON to an json file")
filename = 'package_search.json'
if filename:
    # write the json data
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)