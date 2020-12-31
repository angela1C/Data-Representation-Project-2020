# DataRepProject

This repository contains all the files for my submission for the Big Project assessment for the Data Representation module at GMIT as part of the Higher Diploma in Computing and Data Analytics.

The project involved writing a Flask server program that consumes a REST API and creating a web interface. The project links to the Ireland's open data portal at <https://data.gov.ie>, populates a MySql database with some simple tables, then allows a user to interact with the data stored in the database through a web interface. It also allows the user to requeust additional data from the open data portal. There is some information on the Irish open data portal at the bottom of this readme file.

## This repository contains the following files:

- The instructions for the project in pdf format.
- A Flask server application program named `application.py`.
- Data access object (DAO) files written in Python that provide an interface to the database.
- A `requirements.txt` file containing the Python packages required to run the application.
- A `staticpages` folder containing some html pages that use AJAX calls to the server. Also possibly some other static resources.
- A `dbconfig.py` file
- A `.gitignore` file

I have removed additional python files. used in developing this project to keep the repository simple. They are available in a separate repository.

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
This will start the application on http://127.0.0.1:5000/. Go to your browser 





- `deactivate` to leave the virtual environment and go back to using the system wide environment.
 

---


---
## How to use
https://data.gov.ie/dataset
## openDAO
- The python file `openDAO.py` contains functions to call the data.gov.ie open data portal. The API url is https://data.gov.ie/api/3/action/. The three API actions used are `organization_list`, `tag_list` and `package_list`. There are no query parameters required for these 3 api calls.
    * https://data.gov.ie/api/3/action/package_list is used to retrieve the list of all datasets (known as packages) available on the open data portal.
    * https://data.gov.ie/api/3/action/tag_list is used to retrieve a list of tags.
    * https://data.gov.ie/api/3/action/organization_list is used to retrieve a list of organizations or publishers.

The python script calls the API url using the `requests` library which returns JSON data. This is parsed and sent to the MySQL database. The server file `application.py` has three routes that can trigger these functions at  `/orgs_load`, `/tags_load` and  `/dataset_load`. The openDAO.py file also contains code to truncate the database tables before calling the api so as to avoid duplicate data being stored in the table.  The tables are named `org_list`, `tag_list` and `dataset_list`.
The calls to the API returns JSON files containing  of organizations who provide datasets on the open data portal, list of tag words and list of dataset names.

Once the data has been downloaded to the database from data.gov.ie, they can be viewed on a webpage. As the tables are quite long, there are separate pages for viewing tags, viewing organizations and viewing the actual dataset names. 

### Organizations / Publishers.
A Publisher in data.gov.ie is any Irish Public Sector Body who publishes Open Data on this portal.
There are currently 135 publishers of open data. To view the publishers or search for a publisher, go to the page `/searchOrgs.html`. This webpage is linked to 3 routes in the application server program which retrieves data from the `org_list` database table.  
    * `/orgs` to get all organizations
    * `'/orgs/<string:query>'` to find an organization by search query
    *  `'/orgs/<int:id>'` to find an organisation by id.  

### Tags

The `searchTags.html` page is linked to 3 routes in the application server program. 
    * `'/tags/<int:id>'` to find a tag by id
    * `'/tags/<string:char>'` to find a tag by a search query.
    * `'/tags'` to find all tags stored in the `tag_list` database table.

### Datasets

There are currently over ten thousand datasets available on the Irish open data portal under various themes such as environment, society, health, economy etc. 
The list of datasets are stored in a database table named `dataset_list` which was retrieved by calling the https://data.gov.ie/api/3/action/package_list. Note this action only returns the names of the datasets and not the actual datasets. A further call to another api is required to get the actual data.
To get the links to the actual datasets you can call the api using the package_search action with a query parameter. The query paramter can be a tag name, a organization / publisher name or the actual dataset name.


### All




---
## Python Anywhere

mkvirtualenv --python=/usr/bin/python3.8 venv

I managed to get it hosted on Pythonanywhere. It read in the data from the open data portal api organization_load successfully but after that I got server errors.
The log says: mysql.connector.errors.OperationalError: MySQL Connection not available.

So I will come back and do connection pooling


---


Some references from week 11
### Database Connections:

pooling in mysql-connector

https://pynative.com/python-database-connection-pooling-with-mysql/

https://overiq.com/mysql-connector-python-101/connection-pooling-using-connector-python/

### sqlalchemy

https://www.sqlalchemy.org/

https://blog.pythonanywhere.com/121/ (using sqlalchemy on pythonanywhere.com)

https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91



### Sessions

https://www.tutorialspoint.com/flask/flask_sessions.htm


### About the Open Data portal at <https://data.gov.ie>:
Ireland's open data portal aims at promoting innovation and transparency through the publication of Irish Public Sector data in open, free and reusable formats. 

Open data is information that is collected, produced or paid for by government bodies and made freely available for reuse. Almost all data that is not privacy sensitive can be published as open data with an open licence. The digital economy revolves around data. It can be used to help public adminstration work more efficiently and to improve the quality of their services. It also can be used by businesses to enhance their business models or to open new opportunities. Open data also provides information to citizens on matters that concern them such as local government, public services, public transport scheduling etc.

As of today there are over 10,109 datasets published on the portal by 120 publishers under various themes such as Economy and Finance, Energy, Environment,  Education and Sport, Transport, Science and Technology, Health and more.
The datasets are published in various formats including JSON-STAT, PX, csv format as well as some txt files, html, JSON and others. Some of the datasets have APIs. While the datasets can be accessed directly through the open data portal, they can also be accessed using an API. The site is built using [CKAN](https://docs.ckan.org/en/latest/api/) which allows developers to write code that interacts with the open data portal. [CKAN](https://ckan.org) *is a powerful data management system that makes data accessible – by providing tools to streamline publishing, sharing, finding and using data*. CKAN is a tool for making open data websites and is used by national and local governments, research institutions and other organisations who collect a lot of data. Data is published in units called "datasets". Datasets contain "metadata" (information about the data) and a number of "resources" which hold the data itself such as csv, excel, XML, PDF. CKAN can store the data internally or as a link with the resource itself being available somewhere else on the web. (On earlier CKAN versions, datasets were called "packages" and is still used in places today). Normally login is not needed to search and find data but is needed for all publishing functions.

Using the CKAN API you can get JSON-formatted lists of a site’s datasets, groups or other CKAN objects such as a package list, tag list or group list, get a full JSON representation of a dataset, resource or other object and search for packages or resources matching a query. Authorised users such as publishers who can create, update and delete datasets, resources and other objects. There is no authorization required for accessing the data.

To call the CKAN API, post a JSON dictionary in an HTTP POST request to one of the CKAN APIs URLs. The parameters for the API function should be given in the JSON dictionary. CKAN will also return its response in a JSON dictionary.