# DataRepProject
A repo with just the relevant files for the project

Here I am copying just the relevant files for the project from my other folder.

## This repository contains:

## Instructions on running the project:

## Files contained






- `python -m venv venv`

- `source venv/bin/activate`

- `pip install -r requirements.txt` to load a file of packages. I don't need to do this everytime once the virtual environment has been created

- `export FLASK_APP=application`

- `export FLASK_ENV=development`

- `flask run`

- `deactivate` to leave the virtual environment and go back to using the system wide environment.
---

These are the instructions I used for first getting it up and running. 
On the command line terminal:

- `mkdir webApp`
- `cd webApp` - I am moving the main files back out of webapp directory
- `touch .gitignore`
- `echo /venv > .gitignore`
- `touch README.md`
- `python -m venv venv`
- `source venv/bin/activate`
- `pip freeze`
- `pip install flask`
- `pip freeze > requirements.txt`

The requirements.txt file contains the requirements including `requests` and `python-mysql-connector`

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




---
## Python Anywhere

mkvirtualenv --python=/usr/bin/python3.8 venv

I managed to get it hosted on Pythonanywhere. It read in the data from the open data portal api organization_load successfully but after that I got server errors.
The log says: mysql.connector.errors.OperationalError: MySQL Connection not available.

So I will come back and do connection pooling
