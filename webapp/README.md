## Design the API

Create a document outlining the Rest API for 

The Rest API will have functions to:
- Create some tables by calling the data from the open data portal api
- get all the datasets
    * maybe use login details for this part.

- get a dataset by id or name or tag


- Create a row in another table, say selected datasets you want to work with.
- Update the record for the dataset in this table
- Delete a record for a dataset from this table

Action | Method | Url | Sample Params | Sample Return
| -- | -- | -- | -- | -- |
| Get all datasets| GET | /datasets | none | 
| get all tags| GET | /tags | none
| get all organisations| /organizations | none | 

---



### Setting up the web app.
On the command line terminal:
- mkdir webApp
- cd webApp
- touch .gitignore
- echo /venv > .gitignore
- touch README.md
- python -m venv venv
- source venv/bin/activate
- pip freeze
- pip install flask
- pip freeze > requirements.txt



## Make the Flask App with skeleton functions
- See https://flask.palletsprojects.com/en/1.1.x/quickstart/

- Create a basic server file and test it. I called it `application.py`
The server can either be run just by calling `python application.py` or by using environmental variables.

Using environmental variable has the advantage of being able to run differently depending on whether it is in the cloud or on your own machine.
This way you can see `debug=true` when running the code to test but not set to true on the production side. Setting `debug=true` means you don't have to restart the program when you want to test something.

```shell
export FLASK_APP=application
export FLASK_ENV=development
flask run
```
(replace `export` with `set` for Windows.)

## Write the code for each function



## Create the database

```sql
create database opendata;
use opendata;

```

I created the database and the table in mysql.
I loaded the data into the database by reading from the open data api using list_packages api action and in the same script sent to mysql.
See `createPackages.py`
I have moved this  functionality into the dataDAO.py file.

My server is named `application.py`
My DAO is called dataDAO.
So far I have a table populated from the api call to data.gov.ie package_list action.
The functions getAllDatasets and findDatasetById are working.
I will look at getting the data onto a html page and do the ajax functions before expanding on the tables.

I will create another table that will have all the CRUD functions. 
The users should not post or update the main table of datasets.

---
## Link tables
I could probably expand the project later to link the different tables.

package_list api call to data.gov.ie only returns a list of packages.
package_show and package_search expands on some details of a package which perhaps can tie them together.
- **package_search takes a package name returned from package_list or a tag returned from the tag-list or an organization returned from organization_list**
Therefore I should be able to link the tables
package_show takes a package_name from package_list or a package_id from package_search.

## Next!
do html table.


---
## 3 main files
1. DataDAO
2. Server
3. Index.html

### DataDAO.py
- To get the data from the database
- deals with the MySQL connections
- coverting formats:
    * gets the information in the form of a tuple and converts the tuple into JSON and sends that back to the server.
    * The DAO serves out JSON to the server, not tuples or lists

- The functions in the server call the DAO which uses mysql-connector to connect to the database and returns the data back to the server.

### Server.py
- The server serves out JSON to the HTML as a HTTP response.
- keep as simple as possible.
- contains code to maps URLS to functions. Maps HTTP to requests, gets back responses to particular functions and returns back response. These functions can call the DAO which uses MySQL-connector to connect to the database and returns the data back to the server.



- Anything more complicated than mapping urls to functions should be put in another file.
    * When you make an Ajax request from the browser (like getAll()) it will return the data in a JSON format.
    * To make an update such as Create, Update or Delete, the HTML will make a HTTP request and send it up to the server as JSON.
    The server will pass that JSON to the MySQL connector. MySQL converts it into a list (see the DAO lecture) and makes an SQL function out of it, passes that to the MySQL-connector which passes it to the database.

### Index.html
- This will be served down to the browser using the static directory set up in the flask app
- From the browser, HTML makes HTTP requests up to the server using Ajax.
- Uses Ajax to interact with the server.
- Provides user interface

---
## Running
It seems to be important to not have any white space here when setting the Flask App.
- `python -m venv venv`
- `source venv/bin/activate`

- `export FLASK_APP=application`
- `export FLASK_ENV=development`
- `flask run`

It seems to be important to not have any white space here when setting the Flask App. 
You should see the following on the console:

```
 * Serving Flask app "application" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 ```
On occasion I get an error message that I did not provide the FLASK_APP environmental variable.
 `echo $FLASK_APP` will show if the value actually gets stored in the environmental variable. The problem seems to be to do with white space at either side of the `=`. There should be none.


---
- link the tables
- create a form or a link from the tag, org or package table. The user can click on the row and delete or update the table or call the package_search api call to the open data portal
---

On search.html:
enter tag name or id to return the tag id and tag name
This returns from tags/id and tags/char


on `searchDatasets.html` enter a query (a tag) and search for a dataset.
This returns the name of the dataset that is stored in dataset_list table which was populated from package_list API call to data.gov.ie

---
### update

- can get all tags, orgs and dataset names  from list tables 
- can get datasets from datasets table, can search by id, character and delete
- working on update, this is not working yet. Might have enough without it
- also want to trigger package_search api call but might not get around to it




1. Linking to a third party API - yes
2. Storing the data in a database - yes
3. creating a webpage to view that information - yes
    * may not be necessary if outputting to another API or excel spreadsheet etc
4. Performing some update function through the API (Create, Update, Delete)
    * delete is working

Extras:
- A fully working application ...
- The web page looks nice ...
- A more complicated API
- Linking to some third party API
- if the third party requires authentication
- HOSTED ONLINE 


### Next to do!

- PYTHON ANYWHERE