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


@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username']) +\
            '<br><a href="'+'/index.html'+'">home</a>' +\
             '<br><a href="'+url_for('admin')+'">Admin</a>'

    return 'Welcome to the application. <br/> You are not logged in <br/>' +\
        'You can search for datasets, publishers of datasets on the Irish open data portal using the links at the top of the home page.<br/>' +\
        '' +\
        '<br><a href="'+'/home.html'+'">home</a>'


@app.route('/admin')
def admin():
    if not 'username' in session:
        return redirect(url_for('login'))
    
    return 'Welcome ' + session['username'] +\
        '<br><a href="'+url_for('logout')+'">logout</a>' +\
        '<br><a href="'+'/home.html'+'">home</a>' +\
        '<br/>'+\
        'Admin user can login to load the tags at <a href="/tags_load">tags_load<a/>,' +\
        ' the list of datasets at <a href="/packages_load">packages_load<a/> and' +\
        ' the list of publishers / organizations at <a href="/orgs_load">orgs_load<a/>'

# I have doubled up here so need to delete one.
@app.route('/admin',methods=['GET'])
def adminOnly():
    if 'username' in session:
        return render_template("/admin.html")
    elif not 'username' in session:
        return redirect(url_for('login'))


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username][1] == password:
            session['username'] = username
            return redirect(url_for('admin'))
    return render_template("/login.html")
	
   
# implement logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect('/index.html')


@app.route('/clear')
def clear():
    #session.clear()
    session.pop('counter',None)   

    return "done" 


@app.route('/packages_load',methods=['GET'])
def loadPackages():

    if not 'username' in session:
        #abort(401)
        return redirect(url_for('login'))
        
    elif 'username' in session:
        openDAO.truncateDatasetsTable()
        openDAO.loadDatasetsTable()
        return "The dataset_list table has been loaded from Irish Open data portal " +\
        '<br><a href="'+url_for('logout')+'">logout</a>' +\
        '<br><a href="/home.html">home</a>'

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
        '<br><a href="/home.html">home</a>'




@app.route('/orgs_load', methods=['GET'])
def loadOrgs():
    if 'username' in session:
    # clear table if already populated so it is not duplicated
        openDAO.truncateOrgsTable()
        openDAO.loadOrgsTable()
        return "The org_list table has been loaded from Irish Open data portal " +\
        '<br><a href="'+url_for('logout')+'">logout</a>' +\
        '<br><a href="/home.html">home</a>'

    elif not 'username' in session:
        #abort(401)
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


# this reads from the dataset_list table that contains just the package_name returned from the package_search api
@app.route('/packages/', methods=['GET'])

def getAllDatasetNames():
    results = dataDAO.getAllDatasetNames()
    return jsonify(results)

# returns all datasets containing the string in the package_name field of dataset_list
@app.route('/packages/<string:query>', methods=['GET'])
def findDatasetByName (query):
    foundDatasets = dataDAO.findDatasetByName(query)
    if len(foundDatasets) == 0:
        return jsonify({}) , 204
    return jsonify(foundDatasets)

# this uses the internal database id, not from the open data portal
@app.route('/packages/<int:id>', methods=['GET'])
def findDatasetById(id):
    foundDataset = dataDAO.findDatasetById(id)
    if len(foundDataset) == 0:
        return jsonify({}) , 204
    return jsonify(foundDataset)


#######################################################################
# show resources / datasets with csv or json datasets       DATASETS table
@app.route('/resourceUrls', methods=['GET','DELETE'])
def findDatasetUrls():
    foundDatasetUrls = dataDAO.getDatasetUrls()
    if len(foundDatasetUrls) == 0:
        return jsonify({}) , 204
    return jsonify(foundDatasetUrls)  

# show all datasets in datasets tables  WORKING
@app.route('/resources')
def findAllResources():
    foundResource = dataDAO.getAllResources()
    if len(foundResource) == 0:
        return jsonify({}) , 204
    return jsonify(foundResource)

# find dataset by id. This uses the 36 character id for example "00edfc4d-2083-494c-a466-f748c73fd489"
# This is the id of the dataset retrieved using the package_search api call to data.gov.ie
@app.route('/resources/<string:id>', methods=['GET'])
def findResourceById(id):
    foundResource = dataDAO.findResourceById(id)
    if len(foundResource) == 0:
        return jsonify({}) , 204
    return jsonify(foundResource)


# find dataset by query FIND A DATASET FROM DATASETS WHERE NAME LIKE %S
# As the id search above also uses a string query, I needed to set up a different route here.
@app.route('/queryresources/<string:query>', methods=['GET'])
def findDatasetResource(query):
    foundResource = dataDAO.findDatasets(query)
    if len(foundResource) == 0:
        return jsonify({}) , 204
    return jsonify(foundResource)


#@app.route('/deleteresources/<string:id>', methods=['GET','PUT','DELETE'])
@app.route('/deleteresources/<string:id>', methods=['DELETE'])

def deleteResource(id):
    # this will only delete from the database if the user admin is logged in
    if 'username' in session:
   
    
        dataDAO.deleteResource(id)
        return jsonify({"done":True})
    
    else:
        abort(401)



# @app.route('/external_search/<string:query>')

@app.route('/external/<string:query>',methods=['GET','POST'])
def findExternalDatasetResource(query):

    foundResource = searchDAO.datasetSearch(query)
    
    return "done"




if __name__ == "__main__":
 
    app.run(debug=True)