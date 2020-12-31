from dataDAO import dataDAO
from openDAO import openDAO
from searchDAO import searchDAO


from flask import Flask, url_for, request, redirect, abort, jsonify, render_template, session
from markupsafe import escape
#from flask_cors import CORS
app = Flask(__name__, static_url_path='', static_folder='staticpages')
app.secret_key='dataeverywhere'
# map username to user data
users = {"admin":("admin","1234")}


# https://blog.tecladocode.com/how-to-add-user-logins-to-your-flask-website/
# land the user back to the login page

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username']) +\
            '<br><a href="'+'/index.html'+'">home</a>' +\
             '<br><a href="'+url_for('admin')+'">Admin</a>'

    return 'You are not logged in' +\
        '<br><a href="'+'/index.html'+'">home</a>'


@app.route('/admin')
def admin():
    if not 'username' in session:
        return redirect(url_for('login'))
    
    return 'welcome ' + session['username'] +\
        '<br><a href="'+url_for('logout')+'">logout</a>'

    #return render_template("home.html", name=session.get("username", "Unknown"))



@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username][1] == password:
            session['username'] = username
            return redirect(url_for('admin'))
    return render_template("login.html")
	
   
# implement logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect('/index.html')
    return redirect(url_for('index'))


@app.route('/clear')
def clear():
    #session.clear()
    session.pop('counter',None)   

    return "done" 

#@app.route('/') 
#def index():
#   return "welcome!"

## THIS IS POPULATING THE TABLES FROM THE API

# This is coming from openDAO - maybe have admin access to do this
# Have the tables loaded before the server runs, only admin access then to run it
#get all packages - The list of packages are returned from the open data portal api.
@app.route('/packages_load',methods=['GET'])
def loadPackages():

    if not 'username' in session:
        #abort(401)
        return redirect(url_for('restricted'))
        
    elif 'username' in session:
        openDAO.truncateDatasetsTable()
        openDAO.loadDatasetsTable()
        return "The dataset_list table has been loaded from Irish Open data portal "

@app.route('/tags_load',methods=['GET'])
def loadTags():
    if not 'username' in session:
        return redirect(url_for('login'))

    # clear table if already populated so it is not duplicated
    elif 'username' in session:
        openDAO.truncateTagsTable()
        openDAO.loadTagsTable()
        return "The tag_list table has been loaded from Irish Open data portal " +\
        '<br><a href="'+url_for('logout')+'">logout</a>' +\
        '<br><a href="'+url_for('index')+'">index</a>'




@app.route('/orgs_load', methods=['GET'])
def loadOrgs():
    if 'username' in session:
    # clear table if already populated so it is not duplicated
        openDAO.truncateOrgsTable()
        openDAO.loadOrgsTable()
        return "The org_list table has been loaded from Irish Open data portal "

    elif not 'username' in session:
        #abort(401)
        return redirect(url_for('login'))


@app.route('/admin',methods=['GET'])
def adminOnly():
    if 'username' in session:
        return redirect(url_for('home'))
    elif not 'username' in session:
        return redirect(url_for('login'))


## the tag route

@app.route('/tags',methods=['GET'])
def getAllTags():
    results = dataDAO.getAllTags()
    return jsonify(results)

@app.route('/tags/<int:id>',methods=['GET'])
def findTagById(id):
    foundTag = dataDAO.findTagById(id)
    if len(foundTag) == 0:
        return jsonify({}) , 204
    return jsonify(foundTag)


@app.route('/tags/<string:char>', methods=['GET'])
def findTagByChar(char):
    foundTag = dataDAO.findTagByChar(char)
    if len(foundTag) == 0:
        return jsonify({}) , 204
    return jsonify(foundTag)


## The organisations route - to retrieve data about publishers of open data on data.gov.ie
# data is stored in the org_list table.
@app.route('/orgs',methods=['GET'])

def getAllOrgs():
    results = dataDAO.getAllOrgs()
    return jsonify(results)

@app.route('/orgs/<int:id>',methods=['GET'])
def findOrgById(id):
    foundOrg = dataDAO.findOrgById(id)
    if len(foundOrg) == 0:
        return jsonify({}) , 204
    return jsonify(foundOrg)

@app.route('/orgs/<string:query>',methods=['GET'])
def findOrgs(query):
    foundOrgs = dataDAO.findOrgs(query)
    if len(foundOrgs) == 0:
        return jsonify({}) , 204
    return jsonify(foundOrgs)


# this now reads from the dataset_list table that contains just the package_name returned from the package_search api
@app.route('/datasets/', methods=['GET'])

def getAllDatasets():
    results = dataDAO.getAllDatasets()
    return jsonify(results)

# returns all datasets containing the string in the package_name field of dataset_list
@app.route('/datasets/<string:query>', methods=['GET'])
def findDatasets(query):
    foundDatasets = dataDAO.findDatasets(query)
    if len(foundDatasets) == 0:
        return jsonify({}) , 204
    return jsonify(foundDatasets)

@app.route('/datasets/<int:id>', methods=['GET'])
def findDatasetById(id):
    foundDataset = dataDAO.findDatasetById(id)
    if len(foundDataset) == 0:
        return jsonify({}) , 204
    return jsonify(foundDataset)


#######################################################################
# show resources / datasets with csv or json datasets       DATASETS table
@app.route('/datasetUrls', methods=['GET','DELETE'])
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

# find dataset by id. This uses the 36 character id for example "00edfc4d-2083-494c-a466-f748c73fd489"
# This is the id of the dataset retrieved using the package_search api call to data.gov.ie
@app.route('/dataset_resources/<string:id>')
def findResourceById(id):
    foundResource = dataDAO.findResourceById(id)
    if len(foundResource) == 0:
        return jsonify({}) , 204
    return jsonify(foundResource)


# find dataset by query FIND A DATASET FROM DATASETS WHERE NAME LIKE %S
# As the id search above also uses a string query, I needed to set up a different route here.
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
    if len(foundResource) == 0:
        return jsonify({}) , 204
   
    return jsonify(foundResource)

# DELETE IS WORKING FROM TABLE ON INDEX.HTML

#@app.route('/deleteresources/<string:id>', methods=['GET','PUT','DELETE'])
@app.route('/deleteresources/<string:id>', methods=['DELETE'])

def deleteResource(id):
    # this will only delete from the database if the user admin is logged in
    if 'username' in session:
   
    
        dataDAO.deleteResource(id)
        return jsonify({"done":True})
    
    else:
        abort(401)


# update is NOT working yet, COME BACK TO THIS
@app.route('/update_resource/<string:id>', methods=['PUT','POST'])
def updateResource(id):
    foundResource =dataDAO.findResourceById(id)
    if not foundResource:
        abort(404)

    if not request.json:
        abort(400)


    reqJson = request.json.get('Description')
    return jsonify
    if'Description' in reqJson:
        foundResource['Description'] = reqJson['Description']
    values=(foundResource['Description'])
    dataDAO.updateResource(values)
    return jsonify({"done":True})

    #return jsonify(foundResource)

# The idea is to take a query in by form and send a request to the package_search api to open data portal
@app.route("/resources")
def datasetResourceSearch():
    return "hello"

# HERE! this is working
### this is using a different route to the same one at the top of this file
# @app.route('/external_search/<string:query>')

@app.route('/resources/<string:query>',methods=['GET','POST'])
def findExternalDatasetResource(query):

    foundResource = searchDAO.datasetSearch(query)
    
    return "done indeed"




if __name__ == "__main__":
 
    app.run(debug=True)