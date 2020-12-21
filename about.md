

* The folder "getOpenData" includes some python scripts for interacting with the Irish open data API 'https://data.gov.ie/api/3/action/' using the different actions. These scripts will also create json, xls or csv files from the returned data.
This is where I did most of the preliminary work for the project.


* The folder "webapp" includes the functions that read the data from the open data portal and store in a database.


* The webapp folder contains the following files:

- An  `initdb.sql` file containing the SQL to create the database.
- Various python scripts to get the list of datasets, tags, organizations from the open data portal at data.gov.ie
- The `application.py` Flask App
- A Static pages folder containing an index.html page and various other html pages for the web interface. Ajax calls are used for interacting with the database and performing crud operations.
    * index.html
    * ...html  detail these later

- A datasetDAO.py program for interfacing with the database
- An opendataDAO.py program for retrieving from the Irish open data portal and interfacing with the database

- A requirements.txt file 
- config.py for holding the initial settings, database login etc.


## API action calls to data.gov.ie

See openDataPortalOverview.md in my original repository for background on the Irish open data portal.


### API action calls to data.gov.ie

There are several action apis including `package_list`, `tag_list` and `organization_show` which returns a list of packages/datasets, tags and organisations / dataset providers respectively that exist on the data.gov.ie open data portal.

I have functions to call these 3 apis in the script `openDataLists.py` which calls the three apis and returned the lists of packages, tags and organisations to 3 separate json file. I will use this in my app to populate three database tables. There are also 3 separate files:

- `packageList.py` which just gets the list of packages
- `tagList.py` which just retrieves the list of tags and
- `organisationList.py` which just gets the list of organisations who publish data. (spelt with a z!)
There are some other API action calls which use a query parameter that show more details on an item returned from the above list api calls or searches for a particular resource.

The format of the datasets are not included in the list of packages / datasets so you cannot see if the file is a csv file, or json or px or some other type. However you can use the name returned as a parameter in another api action call to get more information.

- `package_search`
Using the package_search API call you can search for a dataset by providing either a package name returned from the package_list action or a tag name returned from the tag_list action. It is provided as a query parameter ('q') to the package_search api action call.

For example:

- The url "https://data.gov.ie/api/3/action/package_search?q=atmospheric conditions and meteorological geographical features" uses a package name returned from package_list
- "https://data.gov.ie/api/3/action/package_search?q=museum" uses a tag name returned from tag_list.
- See `packageSearch.py` and `getDatasets.py`. I will lose one of these possibly. In getDatasets.py I create csv and excel files with the list of datasets.

- The json data returned will include the url to the actual dataset and the format under the `results['result']['resources']` keys

- `package_show`: The `package_show` action returns a full JSON representation of a dataset. It takes an 'id' query parameter which can be the a dataset name returned from the package_list api or a package_id returned from the package_search api call.
For example, where abbeyfeale-presbytery-rainfall-data is a dataset name returned in the list of datasets / packages, use ?id= followed by the dataset name. For example: data.gov.ie/api/3/action/package_show?id=abbeyfeale-presbytery-rainfall-data

- In `datasetSearch.py` I used the package_search api to get details for all datasets using a query parameter. From the JSON returned I extracted the list of "results" and from each item in results extracted the list of resources. Then I exported some fields to an excel file including the list of urls, some of which have datasets in csv, json, px or other formats. This will work with a full dataset name as the parameter or even a partial name (which might correspond with the tag names returned from tag_list api call - although I tried it with a partial match to a tag and it still returns .)

- `tag_show`: The tag_show action takes a tag returned from the tag_list action as an 'id' query parameter. It returns some JSON about the tag. I don't think it is very useful.
Although there may be spaces in the tags returned from the tag_list, the tag name does not seem to need to be encoded. If you paste the full url into the browser, it shows the spaces encoded as "%20" but the python script will take the full url without any encoding. For example : "https://data.gov.ie/api/3/action/tag_show?id=atmospheric conditions and meteorological geographical features"

See tagShow.py for a python script

- `organization_show`:
An organization name can be taken from the organization_list api call and used as a id query parameter in the organization_show api action. It returns details on 'users' at the organization. It is not very useful. For example: 'https://data.gov.ie/api/3/action/organization_show?id=central-bank-of-ireland'

### List of resources

Using the `resource_search` api with a query = name parameter, you can search for resources matching the query key with the value being the name of a tag returned from the tag_list. I am just taking the resource url and the name of the dataset. For this reason I limited the number of rows written to a csv file. Not all tags with return a list of datasets and some tags have a huge number of associated datasets, for example rainfall.

For example:

"https://data.gov.ie/api/3/action/resource_search?query=name:alcohol"

Note here the query parameter follows ?query=name: rather than a 'q' or 'id' as in the other api action calls that used parameters. I appended the query parameters to the API url instead of using the dictionary keys as I did for others as I couldn't get it to work the other way.

Using the "https://data.gov.ie/api/3/action/resource_search?query=name:" without any tag parameter will return a very very large JSON file with all of the resources. This is a huge file!

I tested it using a single word query such as 'alcohol' or 'rainfall' or 'rivers' etc and this works to pull an object that contains the url for any datasets matching these tags.