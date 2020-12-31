# DataRepProject

By Angela Carpenter G00376372

This repository contains all the files for my submission for the Big Project assessment for the Data Representation module at GMIT as part of the Higher Diploma in Computing and Data Analytics.

The project involved writing a Flask server program that consumes a REST API and creating a web interface. The project links to the Ireland's open data portal at <https://data.gov.ie>, populates a MySql database with some simple tables, then allows a user to interact with the data stored in the database through a web interface. It also allows the user to request additional data from the Irish open data portal. There is some information on the Irish open data portal at the bottom of this readme file and in the [About Irelands Open Data portal](aboutIrelandsOpenDataPortal.md) file attached.

## This repository contains the following files:

- The instructions for the project in [pdf](project_description.pdf) format.
- A Flask server application program named `application.py`.
- Data access object (DAO) files written in Python that provide an interface to the database.
- A `requirements.txt` file containing the Python packages required to run the application.
- A `staticpages` folder containing some html pages for the web application that use AJAX calls to the server. 
- A `dbconfig.py` file
- A `.gitignore` file
- An `initdb.sql` file containing the SQL to create the database.
- A `datasetDAO.py` program for interfacing with the database.
- An `opendataDAO.py` program for retrieving JSON data from the Irish open data portal using the `tag_list`, `package_list` and `organization_list` actions and interfacing with the database.
- A `searchDAO.py` program for retrieving JSON data from the open data portal using the `package_search` api action together with a search query parameter.


I have removed all additional Python files that were used in developing this project to keep the repository simple. They are still available in a separate repository.

## Instructions on running the project:

The repository can be downloaded from my Github account at https://github.com/angela1C/DataRepProject
by clicking the green `Code` button and following the instructions to clone the repo.

The `requirements.txt` file contains the Python requirements including `Flask`,`requests` and `python-mysql-connector`.

Activate a virtual environment using the following commands on the command line:

- `python -m venv venv` to create a blank virtual environment with a directory named `venv`.

- `source venv/bin/activate` on Mac/Linux or `.\venv\Scripts\activate.bat` on Windows.

- `pip install -r requirements.txt` to install the file of Python packages.

- `export FLASK_APP=application` to set the server environmental variable. On Windows use `set` instead of `export`. Make sure there are no spaces. 

- `export FLASK_ENV=development` to run in a development environment.

- `flask run` to run the server program. 
This will start the application on http://127.0.0.1:5000/. Copy the link into your browser. Click the link to access the web interface.

- To stop the server running, use `ctrl` + `c`.

- `deactivate` to leave the virtual environment and go back to using the system wide environment.
 
---
## How to use the web application:

There are three DAO files. The first one `openDAO` contains functions to call the <data.gov.ie> open data portal. The API url is https://data.gov.ie/api/3/action/. The three API actions used are `organization_list`, `tag_list` and `package_list`. There are no query parameters required for these 3 api calls.
* https://data.gov.ie/api/3/action/package_list is used to retrieve the list of all datasets (known as packages) available on the open data portal.
* https://data.gov.ie/api/3/action/tag_list is used to retrieve a list of tags.
* https://data.gov.ie/api/3/action/organization_list is used to retrieve a list of organizations or publishers.

The python script calls the API url using the `requests` library which returns JSON data. This is parsed and sent to the MySQL database. 
- The server file `application.py` contains three routes that can trigger these functions at  `/orgs_load`, `/tags_load` and  `/dataset_load`. An `admin` user needs to be logged in to trigger these functions. You can also go  directly to `/admin` to load these tables.
- The `openDAO.py` file also contains code to truncate the database tables before calling the api so as to avoid duplicate data being stored in the table.  The tables are named `org_list`, `tag_list` and `dataset_list`.
The calls to the API returns JSON files containing  the lists of organizations or publishers who provide datasets on the open data portal, list of tag words and list of the names of the datasets.

Once the data has been downloaded to the database from <data.gov.ie>, the JSON data can be viewed in the browser. 
There are also webpages for viewing and finding tags, publishers or datasets. The links are available in the navigation bar of the webpages. 

### Tags:
- The list of  `tags` is available at `/tags` in JSON format. 
- Select `Tags` from the navigation bar to enter a search for a tag. Without entering a query, you will get a list of all the tags. There are over 8,600 tags so this is a long list. Use the form to narrow the search. The `%` can be used as a wildcard. For example use `a` to find all tags beginning with the letter `a`, use `air` to find all tags beginning with `air`, use `%air` to find all tags containing `air`. Refresh the page if you want to search again as the tags are appended to the end of the table or scroll down the page.

### Organizations / Publishers
- The list of organizations or publishers is available at `/orgs` in JSON format.
- Select `Publishers` from the navigation bar to enter a search for a particular publisher of open data. The search function works in the same way as the tags above.

### Datasets
- The list of datasets or packages is available  at `/datasets` in JSON format.

The JSON data can also be viewed be viewed using the '/datasets' route. 

### Organizations / Publishers.
A Publisher in data.gov.ie is any Irish Public Sector Body who publishes Open Data on this portal.
There are currently 135 publishers of open data. To view the publishers or search for a publisher, go to the page `/searchOrgs.html`. This webpage is linked to 3 routes in the application server program which retrieves data from the `org_list` database table.  
    * `/orgs` to get all organizations
    * `'/orgs/<string:query>'` to find an organization by search query
    *  `'/orgs/<int:id>'` to find an organisation by id.  

### Tags

The `searchTags.html` page is linked to 3 routes in the application server program. 
- `'/tags/<int:id>'` to find a tag by id
- `'/tags/<string:char>'` to find a tag by a search query.
- `'/tags'` to find all tags stored in the `tag_list` database table.

### Datasets

There are currently over ten thousand datasets available on the Irish open data portal under various themes such as environment, society, health, economy etc. 
The list of datasets are stored in a database table named `dataset_list` which was retrieved by calling the <https://data.gov.ie/api/3/action/package_list>. Note this action only returns the names of the datasets and not the actual datasets. A further call to another api using the action `package_search` is required to retrieve a JSON representation of the dataset. This will return details about the dataset including the dataset format, a description if available, the dataset id, a package id and a URL to the actual dataset. This data is stored in the `datasets` table in the database. This is a different table to the dataset_list table which contains only the dataset or package name as returned by the call to the package_list api.

To get the links to the actual datasets you can call the api [data.gov.ie/api/action](https://data.gov.ie/api/3/action/) using the `package_search` action together with a query parameter. The query parameter can be a tag name, a organization / publisher name or the actual dataset name. 

Any datasets that have been already retrieved using the `package_search` api are stored in the `datasets` table. Therefore this may be empty on first use. To populate this table, the server uses a function in the `searchDAO` file. You can enter a query using the `/external/` route. The query can be a dataset name, an organization name or a tag name. This functionality can also be accessed  using the `External` nav links to at the top of each page and entering a query into the form. 

The list of datasets that have been already retrieved can be viewed and searched on the `search.html` page. The user can enter a search query into the form. This should be in lower case. The `%` can be used as a wildcard to narrow the search. The table returned contains the URL to the actual dataset and some details about the dataset. An admin user who is logged in can delete a record from the database. A normal user can delete a record from the table but it will not be deleted from the database. The table includes the URLs to the datasets. To download a dataset you can navigate to the link in your own browser or clicking on the link. Please note that some of these datasets can be very large.


---
## Python Anywhere

While I did manage to briefly get the application hosted on Python Anywhere, it is not currently working properly. I initially used the free tier but quickly ended up in the tarpit!. Therefore I upgraded the account to access the premium services and this allowed me to get the application running and get some of the database tables populated by calling the <data.gov.ie> API. However after trying out some of the functions on the web pages, the application stopped working as I exceeded the max user connections in the connection pool. I do intend to return to this to get it working, at least to get my money's worth! 
If I do get it working it will be available at [angela1C.pythonanywhere.com](http://angela1c.pythonanywhere.com).

Because connection pooling has been set up to worj with PythonAnywhere, when running the application locally, it is possible that you may need to restart the server if the connection pool gets exhausted. This can be restarted using `flask run`.


---

### About the Open Data portal at <https://data.gov.ie>:
Ireland's open data portal aims at promoting innovation and transparency through the publication of Irish Public Sector data in open, free and reusable formats. 

Open data is information that is collected, produced or paid for by government bodies and made freely available for reuse. Almost all data that is not privacy sensitive can be published as open data with an open licence. The digital economy revolves around data. It can be used to help public adminstration work more efficiently and to improve the quality of their services. It also can be used by businesses to enhance their business models or to open new opportunities. Open data also provides information to citizens on matters that concern them such as local government, public services, public transport scheduling etc.

As of today there are over 10,109 datasets published on the portal by 120 publishers under various themes such as Economy and Finance, Energy, Environment,  Education and Sport, Transport, Science and Technology, Health and more.
The datasets are published in various formats including JSON-STAT, PX, csv format as well as some txt files, html, JSON and others. Some of the datasets have APIs. While the datasets can be accessed directly through the open data portal, they can also be accessed using an API. The site is built using [CKAN](https://docs.ckan.org/en/latest/api/) which allows developers to write code that interacts with the open data portal. [CKAN](https://ckan.org) *is a powerful data management system that makes data accessible – by providing tools to streamline publishing, sharing, finding and using data*. CKAN is a tool for making open data websites and is used by national and local governments, research institutions and other organisations who collect a lot of data. Data is published in units called "datasets". Datasets contain "metadata" (information about the data) and a number of "resources" which hold the data itself such as csv, excel, XML, PDF. CKAN can store the data internally or as a link with the resource itself being available somewhere else on the web. (On earlier CKAN versions, datasets were called "packages" and is still used in places today). Normally login is not needed to search and find data but is needed for all publishing functions.

Using the CKAN API you can get JSON-formatted lists of a site’s datasets, groups or other CKAN objects such as a package list, tag list or group list, get a full JSON representation of a dataset, resource or other object and search for packages or resources matching a query. Authorised users such as publishers who can create, update and delete datasets, resources and other objects. There is no authorization required for accessing the data.

To call the CKAN API, post a JSON dictionary in an HTTP POST request to one of the CKAN APIs URLs. The parameters for the API function should be given in the JSON dictionary. CKAN will also return its response in a JSON dictionary.
The api actions used for this web application are the `package_list`, `tag_list` and `organization_list` as well as the `package_search` action with a query parameter as outlined earlier. There are some other api actions that I did not use for the final application. See [aboutIrelandsOpenDataPortal](aboutIrelandsOpenDataPortal.md) for further information. 

---
## References

- The primary reference for this project is the lecture notes by Lecturer Andrew Beatty of the Data Representation module at GMIT and the notes and code available at [Data Representation2020](https://github.com/andrewbeattycourseware/dataRepresenation2020)

- The [Irish Open Data portal](https://data.gov.ie)at data.gov.ie

- The [developer's corner](https://data.gov.ie/developer) at data.gov.ie
- The [developer's resources ](https://data.gov.ie/pages/developers). This provides some information on how to use the API.
- [Flask Quickstart](https://flask.palletsprojects.com/en/1.1.x/quickstart/#logging) at https://flask.palletsprojects.com
- [CKAN](https://docs.ckan.org/en/latest/api/) at https://docs.ckan.org
- [Flask Tutorial](https://www.tutorialspoint.com/flask/index.htm) at https://www.tutorialspoint.com
- [Introduction to Bootstrap4](https://getbootstrap.com/docs/5.0/getting-started/introduction/) at https://getbootstrap.com



- [Python Database Connection Pooling with MySQL](https://pynative.com/python-database-connection-pooling-with-mysql/)
- [Connection Pooling](https://overiq.com/mysql-connector-python-101/connection-pooling-using-connector-python/)







