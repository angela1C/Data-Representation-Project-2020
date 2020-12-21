"""
Nov 26th

This API call gives a details of the organization, its status, number of resources, packages/datasets, type of datasets and more
"""
import requests
import json
import sys


def organisation_details(url, param): # Action: organization_show
    
    try:
        
        response = requests.get(url+'organization_show', params)
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

            

    except SystemError:
        print("Bad request - check organization name returned from organization_list request")
        sys.exit(1)
        
    except Exception as e:
        print(e)
        sys.exit(1)
        

params = {'id': 'coca-cola-zero-bikes'}        
organisation_details('https://data.gov.ie/api/3/action/', params)

