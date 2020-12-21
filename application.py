from dataDAO import dataDAO
from openDAO import openDAO
from searchDAO import searchDAO


from flask import Flask, url_for, request, redirect, abort, jsonify
#from flask_cors import CORS
app = Flask(__name__, static_url_path='', static_folder='staticpages')
#CORS(app)

@app.route('/') 
def index():
    return "hello there opendata how are you today"


## THIS IS POPULATING THE TABLES FROM THE API

# This is coming from openDAO - maybe have admin access to do this
# Have the tables loaded before the server runs, only admin access then to run it
#get all packages - The list of packages are returned from the open data portal api.
@app.route('/packages_load')
def loadPackages():
    openDAO.truncateDatasetsTable()
    #print("cleared dataset_list table")
    openDAO.loadDatasetsTable()
    return "The dataset_list table has been loaded from Irish Open data portal "

@app.route('/tags_load')
def loadTags():
    # clear table if already populated so it is not duplicated
    openDAO.truncateTagsTable()
    openDAO.loadTagsTable()
    return "The tag_list table has been loaded from Irish Open data portal "


@app.route('/orgs_load')
def loadOrgs():
    # clear table if already populated so it is not duplicated
    openDAO.truncateOrgsTable()
    openDAO.loadOrgsTable()
    return "The org_list table has been loaded from Irish Open data portal "


@app.route('/external_search')
def datasetSearch():
    openDAO.datasetSearch()  
    print("hello there")

## the tag route

@app.route('/tags')

def getAllTags():
    results = dataDAO.getAllTags()
    return jsonify(results)

@app.route('/tags/<int:id>')
def findTagById(id):
    foundTag = dataDAO.findTagById(id)
    if len(foundTag) == 0:
        return jsonify({}) , 204
    return jsonify(foundTag)


@app.route('/tags/<string:char>')
def findTagByChar(char):
    foundTag = dataDAO.findTagByChar(char)
    if len(foundTag) == 0:
        return jsonify({}) , 204
    return jsonify(foundTag)


## The org route
@app.route('/orgs')

def getAllOrgs():
    results = dataDAO.getAllOrgs()
    return jsonify(results)

@app.route('/orgs/<int:id>')
def findOrgById(id):
    foundOrg = dataDAO.findOrgById(id)
    if len(foundOrg) == 0:
        return jsonify({}) , 204
    return jsonify(foundOrg)

@app.route('/orgs/<string:query>')
def findOrgs(query):
    foundOrgs = dataDAO.findOrgs(query)
    if len(foundOrgs) == 0:
        return jsonify({}) , 204
    return jsonify(foundOrgs)


# this now reads from the big table that contains just the package_name returned from the package_search api
@app.route('/datasets/')

def getAllDatasets():
    results = dataDAO.getAllDatasets()
    return jsonify(results)

# returns all datasets containing the string in the package_name field of dataset_list
@app.route('/datasets/<string:query>')
def findDatasets(query):
    foundDatasets = dataDAO.findDatasets(query)
    if len(foundDatasets) == 0:
        return jsonify({}) , 204
    return jsonify(foundDatasets)

@app.route('/datasets/<int:id>')
def findDatasetById(id):
    foundDataset = dataDAO.findDatasetById(id)
    if len(foundDataset) == 0:
        return jsonify({}) , 204
    return jsonify(foundDataset)


#######################################################################
# show resources / datasets with csv or json datasets
@app.route('/datasetUrls')
def findDatasetUrls():
    foundDatasetUrls = dataDAO.getDatasetUrls()
    if len(foundDatasetUrls) == 0:
        return jsonify({}) , 204
    return jsonify(foundDatasetUrls)  

# show all datasets in datasets tables  WORKING
@app.route('/dataset_resources')
def findAllResources():
    foundResource = dataDAO.getAllResources()
    if len(foundResource) == 0:
        return jsonify({}) , 204
    return jsonify(foundResource)

# find dataset by id        WORKING for id
@app.route('/dataset_resources/<string:id>')
def findResourceById(id):
    foundResource = dataDAO.findResourceById(id)
    if len(foundResource) == 0:
        return jsonify({}) , 204
    return jsonify(foundResource)


# find dataset by query     WORKING now with a new route
@app.route('/dataset_resources_query/<string:query>')
def findDatasetResource(query):
    foundResource = dataDAO.findADataset(query)
    if len(foundResource) == 0:
        return jsonify({}) , 204
    return jsonify(foundResource)

# working with id
@app.route('/myresources/<string:id>', methods=['GET','PUT','DELETE'])
def findById(id):
    foundResource = dataDAO.findResourceById(id)
   
    return jsonify(foundResource)

# DELETE IS WORKING FROM TABLE ON INDEX.HTML

#@app.route('/deleteresources/<string:id>', methods=['GET','PUT','DELETE'])
@app.route('/deleteresources/<string:id>', methods=['DELETE'])
def deleteResource(id):
    dataDAO.deleteResource(id)
    return jsonify({"done":True})


# update is NOT working yet
@app.route('/updateresource/<string:id>', methods=['PUT'])
def updateResource(id):
    foundResource =dataDAO.findResourceById(id)
    if not foundResource:
        abort(404)

    if not request.json:
        abort(400)

    reqJson = request.json
    if'Description' in reqJson:
        foundResource['Description'] = reqJson['Description']
    values=(foundResource['Description'])
    dataDAO.update(values)

    return jsonify(foundResource)






@app.route("/resources")
def datasetResourceSearch():
    return "hello"

@app.route('/resources/<string:query>')
def findExternalDatasetResource(query):

    foundResource = searchDAO.datasetSearch(query)
    if len(foundResource) == 0:
        return jsonify({}) , 204
    return jsonify(foundResource)





# create dataset
# curl -H "Content-Type:application/json" -X POST -d "{\"Name\":\"Testing creating a dataset\"}" http://127.0.0.1:5000/datasets
@app.route('/datasets', methods=['POST'])
def create():
    global nextId
    if not request.json:
        abort(400)
    
    dataset = {
        "id": nextId,
        "Name": request.json["Name"]
    }
    datasets.append(dataset)
    nextId += 1
    return jsonify(dataset)


#update dataset

@app.route('/datasets/<int:id>', methods=['PUT']) 
def update(id):
    return "served by update with id " + str(id)

# delete dataset
@app.route('/datasets/<int:id>', methods=['DELETE']) 
def delete(id):
    return "served by delete with id " + str(id)

# curl -H "Content-Type:application/json" -X PUT -d '{"{Name":"testing1234"}' http://127.0.0.1:5000/datasets/1





if __name__ == "__main__":
 
    app.run(debug=True)