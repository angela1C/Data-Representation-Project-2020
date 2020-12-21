"""
Get the list of datasets / packages using `package_search` action and a query parameter.
The query parameter 'q' can be  a package name returned from package_list or a tag name returned from tag_list.
The function also saves the list of datasets to excel and csv.

The API url is https://data.gov.ie/api/3/action/package_search plus whatever query parameters.




"""
import requests
import json
import sys






def getDataset(url, paramss): # Action
    
    try:
        # for now include the action in the url
        response = requests.get(url+'package_search',params)
        print(response.status_code)
        data = response.json()
    
        if not data['success']:
            raise SystemError

        if len(data['result']) == 0:
            raise Exception

        else:
           
            print("writing the returned JSON to an json file")
            # create a filename based on the query parameter
            filename = params['q'] + ".json"
            print(filename)
            
            if filename:
            # write the json data
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=4)

            list_of_results = []
            list_of_resources =[]

            #for result in data["result"]["results"]["resources"][3][url]:
            for result in data["result"]["results"]:
                list_of_results.append(result)

                for resource in result['resources']:
                    #print("RESOURCE")
                    #print(resource)
                    list_of_resources.append(resource)



            #print(list_of_resources)   

            # create a file name based on the query parameter

            sheetname = params['q'][0:10] + "_urls."
            print(sheetname)


            w = Workbook()
            ws = w.add_sheet(sheetname)
            

            rowNumber = 0;
            ws.write(rowNumber,0,"name")
            ws.write(rowNumber,1,"url")
            ws.write(rowNumber,2,"package_id")
            ws.write(rowNumber,3,"id")
            ws.write(rowNumber,4,"description")
            ws.write(rowNumber,5,"created")
            ws.write(rowNumber,6,"resource_type")
            ws.write(rowNumber,7,"format")
            ws.write(rowNumber,8,"last_modified")  


            rowNumber += 1 
            print("******************************************************\n\n")
            print(f"There are {len(list_of_resources)} items in the list")   
            list_of_urls=[]

            for resource in list_of_resources:
                #print("RESOURCE")
                #print(resource)
                #print("RESOURCE_URL")
                #print(resource['url'])
                ws.write(rowNumber,0,resource["name"])
                ws.write(rowNumber,1,resource["url"])
                ws.write(rowNumber,2,resource["package_id"])
                ws.write(rowNumber,3,resource["id"])
                ws.write(rowNumber,4,resource["description"])
                ws.write(rowNumber,5,resource["created"])
                ws.write(rowNumber,6,resource["resource_type"])
                ws.write(rowNumber,7,resource["format"])
                ws.write(rowNumber,8,resource["last_modified"])   

                rowNumber += 1
            xlsfile = params['q'] + ".xls"
            
            w.save(xlsfile)
            csvfile = params['q']+ ".csv"
            df = pd.read_excel(xlsfile, sheetname)
            df.to_csv(csvfile)


             

    except SystemError:
        print("Failed request. Please check your query parameters")
        sys.exit(1)
        
    except Exception as e:
        print(e)
        sys.exit(1)
        
# the query parameter can be a tag name or a package name
params = {'q': 'commission-for-energy-regulation' }     
myDataset = getDataset('https://data.gov.ie/api/3/action/', params)
