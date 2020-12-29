from dataDAO import dataDAO
from openDAO import openDAO
from searchDAO import searchDAO
import json
print("ok")

testpackage = {
    'id': 4,
    'package': 'changing-datasetname-of-package-number-4'

}



#returnValue = dataDao.getAll()
#sprint(returnValue)

print("done")

#returnValue = dataDao.findById(1011)
#print("find By Id")
#print(returnValue)

#returnValue = dataDao.delete(2)
#print(returnValue)


#testpackage = {'id':4,'package':'changing-datasetname-of-package-number-4'}
    

# update is not working
#returnValue = dataDao.update(testpackage,)
#print(returnValue)

if __name__ =="__main__":

    #openDAO.truncateOrgsTable()
    #print("cleared organizations table")
    #openDAO.loadOrgsTable()
    #print("populated organization table")
    #openDAO.truncateTagsTable()
    #print("cleared tags table")
    #openDAO.loadTagsTable()
    #print("populated organization table")
    #openDAO.truncateDatasetsTable()
    #print("cleared dataset_list table")
    #openDAO.loadDatasetsTable()
    #print("cleared dataset_list table")

    #openDAO.truncateDatasets()
    #print("cleared datasets table")
    #params = {'q': 'accidents' } 
    #openDAO.datasetSearch(url = 'https://data.gov.ie/api/3/action/',action="package_search",params= {'q': 'central-statistics-office' } )
    #openDAO.datasetSearch(url = 'https://data.gov.ie/api/3/action/',action="package_search",params= {'q': 'an-garda-siochana' } )
    #openDAO.datasetSearch(url = 'https://data.gov.ie/api/3/action/',action="package_search",params= {'q': 'department-of-health' } )
    #openDAO.datasetSearch(url = 'https://data.gov.ie/api/3/action/',action="package_search",params= {'q': 'eurostat' } )
    #print("done")
    #datasets = dataDAO.getAllDatasetsUrls()
    #results = datasets
    #colnames=['id','package_id','name','description','url','format','created']
    #item = {}

    #for i in result:

        #print(f"{result['id']}\n")
            
    #return item


    #for colName in enumerate(colnames):
    #    for i in range(len(datasets)):
        

        
    #        value = datasets[i]
    #        item[colName] = value
    #print(type(item))
    #print(item.keys())
    #returnValue = dataDAO.findTagById(1011)
    #print("find By Id")
    #print(returnValue)


    #returnValue = dataDAO.findTagByChar("b%")
    #print("find By char")
    #print(returnValue)

    #params= {'q': 'river' }
    #openDAO.datasetSearch(url = 'https://data.gov.ie/api/3/action/',action="package_search",params=params)
    #query ="bovine"
    

    #dataDAO.findADataset(query)
    #query="family"
    #dataDAO.findDatasets(query)
    

    #print(dataDAO.getAllDatasets())
    #openDAO.loadDatasetsTable(action='package_list')
    #params= {'q': '011-to-2016-by-composition-of-private-household-age-group-of-youngest-child-censusyear-and-statistic' } 
    #openDAO.datasetSea
    #rch(url = 'https://data.gov.ie/api/3/action/',action="package_search",params= {'q': 'central-statistics-office' } )
    
    
    #params = "waterford"
    #result = searchDAO.datasetSearch(params=params)
    #print(result)

    #id = "06fa4c76-c03b-46a3-9dbe-07f76b23eeb6"
    #dataDAO.findResourceById(id)

    #dataDAO.deleteResource(id)

    # UPDATE this is working here
    #values = ("testing updating from python",)
    #id="025f1d0c-1dd7-43d2-a924-5c4ec9217f4b"
    #dataDAO.updateResource(values)

    
    params ="teach"
    result = searchDAO.datasetSearch(params=params)
    print(result)



    

   