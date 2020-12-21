"""
Get the list of packages using the package_list api action.
Save to a json file.
packages are another word for datasets
"""



import requests
import json
from xlwt import *

url = "https://data.gov.ie/api/3/action/"
action = "package_list"
URL_API = url + action
response = requests.get(URL_API)
data = response.json()


print(response.status_code)
data = response.json()
print(data)

print("writing the returned JSON to an json file")
filename = 'package_list.json'
if filename:
    # write the json data
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)