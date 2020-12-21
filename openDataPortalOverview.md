My aim here is to get open data from the [data.gov.ie](https://data.gov.ie/) website. This is Ireland's open data portal *Promoting innovation and transparency through the publication of Irish Public Sector data in open, free and reusable formats*.


There are many datasets listed here in various file formats. Some of them have APIs.
As of today there are 10089 datasets by 117 publishers.

The video on [exploring open data](https://www.youtube.com/watch?v=cIGlt4Y9vVc&feature=youtu.be) provided by the European Data portal outlines some of the benefits of open data.
Open data is information that is collected, produced or paid for by government bodies and made freely available for reuse. Almost all data that is not privacy sensitive can be published as open data with an open licence. The digital economy revolves around data. It can be used to help public adminstration work more efficiently and to improve the quality of their services. It also can be used by businesses to enhance their business models or to open new opportunities. Open data also provides information to citizens on matters that concern them such as local government, public services, public transport scheduling etc. 


The [data.gov.ie/datasets](https://data.gov.ie/) page lists all the datasets under various themes such as Environment, Society, Health, Economy and more.
At the moment there are 9581 datasets without API's and 508 datasets with API's. Datasets are provided in various resource formats with the majority in`JSON-STAT`, `PX`, `csv` format. There are also `txt` files, `html`, `JSON` and many other formats.

At the bottom of the datasets page, there is a note that you can also access this registry using the API and a link to the API docs is provided. This links to the  [CKAN API guide](https://docs.ckan.org/en/latest/api/) website. 

[CKAN](https://docs.ckan.org/en/latest/user-guide.html#what-is-ckan) is a tool for making open data websites and is used by national and local governments, research instiutions and other organisations  who collect a lot of data. Data is published in units called "datasets". Datasets contain "metadata" (information  about the data) and a number of "resources" which hold the data itself such as csv, excel, XML, PDF. CKAN can store the data internally or as a link with the resource itself being available somewhere else on the web. (On earlier CKAN versions, datasets were called "packages" and is still used in places today). Normally login is not needed to search and find data but is needed for all publishing functions.

Using the CKAN API your app can 
- get JSON-formatted lists of a site’s datasets, groups or other CKAN objects:
    * package list
    * group list
    * tag list

- Get a full JSON representation of a dataset, resource or other object:
- Search for packages or resources matching a query
- Create, update and delete datasets, resources and other objects
- Get an activity stream of recently changed datasets on a site.

A guide to making an API request provides  the following instructions and some examples:

### Making an API Request
To call the CKAN API, post a JSON dictionary in an HTTP POST request to one of CKAN APIs URLs. The parameters for the API function should be given in the JSON dictionary. CKAN will also return its response in a JSON dictionary.
The command line client Curl can be used to post a JSON dictionary to a URL.
The response will be a JSON dictionary with three keys:
1. "success": true or false.
The API aims to always return `200 ok` as the status code of it's HTTP response whether or not there were errors in the 
2. "result": the returned result from the function you called. If there was an error in your request, the dictionary will contain an `"error"` key.
3. "help": the documentation string for the function you called.


The same request can be made using Python's standard `urllib2` module. Some code is provided below.

```python
#!/usr/bin/env python
import urllib2
import urllib
import json
import pprint

# Make the HTTP request.
response = urllib2.urlopen('http://demo.ckan.org/api/3/action/group_list',
        data_string)
assert response.code == 200

# Use the json module to load CKAN's response into a dictionary.
response_dict = json.loads(response.read())

# Check the contents of the response.
assert response_dict['success'] is True
result = response_dict['result']
pprint.pprint(result)

```
When  importing many datasets it is usually more efficient to automate the process in some way.

Some API functions require authorisation. This is probably for posting to the API which is not relevant to me for now.

### GET requests
Functions defined in [ckan.logic.action.get](https://docs.ckan.org/en/latest/api/#ckan-logic-action-get) can also be called with an HTTP GET request. You can just open the URL in the browser.

For example use the URL <http://demo.ckan.org/api/3/action/package_search?q=spending>  to search for datasets 
- The search query is given as a URL parameter, for example `?q=spending`.

- Multiple URL parameters can be appended, seperated by ampersands `&`.

For example use URL `http://demo.ckan.org/api/3/action/package_search?q=spending&rows=10` to get only the first 10 matching datasets.

- When an action requires a list of strings as the value of a parameter, the value can be sent by giving the parameter multiple times in the URL:
`http://demo.ckan.org/api/3/action/term_translation_show?terms=russian&terms=romantic%20novel`


---
Datasets
According to the dataset landing page most (9581) of the datasets are without API's while only 508 datasets have API's. Of the 508 datasets with API's, 417 are in CSV format, 398 in ESRI REST format, 205 GEOJSON. There are many other formats mentioned here. The main publisher seems to be South Dublin County Council with 164 datasets, Galway City Council with 52, Ordnance Survey Ireland with 40, Galway County Council with 38, Geological Survey of Ireland with 27 and the rest by various other publishers. I will have first have a look at these datasets with APIs and then have a look at the datasets without API's. API is mentioned as a resource format for 110 of the 508 datasets.


---
The [Developer's Resources](https://data.gov.ie/pages/developers) section outlines how to use the API and provides some example API calls.

### Example API Calls
Here are the examples from the Developer's resources. I will keep them here for reference for now.

### List Datasets on data.gov.ie
- Get JSON-formatted lists of a site’s datasets or other CKAN objects:
    * `data.gov.ie/api/3/action/package_list`. 
    When using curl with `-i` to see the response header, I get a 301 that the page has moved permanently and a link to the `Location: https://data.gov.ie/api/3/action/package_list` url instead. Similarly to get the list of tags, the URL `https://data.gov.ie/api/3/action/tag_list` should be used.

- Get a full JSON representation of a dataset, resource or other object:
    * `data.gov.ie/api/3/action/package_show?id=the-walled-towns-of-ireland`
    * `data.gov.ie/api/3/action/tag_show?id=marine`

- Search for packages or resources matching a query:

    * `data.gov.ie/api/3/action/package_search?q=museum`

    * `data.gov.ie/api/3/action/resource_search?query=name:The%20Walled%20Towns%20of%20Ireland`
---

The [developer's corner](https://data.gov.ie/developer) provides some links to Jupyter Notebook tutorials on Google Colab which serve to introduce the core concepts for connecting to the Data.gov.ie API as well as more advanced usage for the purposes of data enrichment and visualisation.
- The [CKAN_API_Dem](https://colab.research.google.com/github/derilinx/Developer_Corner_DGI/blob/master/CKAN_API_Demo.ipynb) notebook aims to show developers how the data.gov.ie API can be used to extract data for use programmatically.

See <https://derilinx.com/new-features-for-developers-now-available-on-data-gov-ie/>

Note for now I am only looking at the functions in the notebooks to figure out how to use the APIs to get the json files with the actual data down.
I am not doing anything elaborate with the data for now!  Therefore only using the `requests` and the `json` packages. These notebooks do seem a bit out of date as some if the Python packages are deprecated. 
---

# Using the API

The URL for the API is the base URL 'https://data.gov.ie' and '/api/3/action/' plus whatever query parameters you are interested in.
This URL can be used in the browser, on the command line with curl or programmatically. I will be using Python 3.

As mentioned above the response will be a JSON dictionary with the three keys `success`: true or false, `result` with the returned result and `help` with any documentation strings.


- A request is made with three parts to the url: the base url "https://data.gov.ie" + "/api/3/action/" + "organization_list"

- The results array in the returned json object contains a list of all the datasets or tags or organisations etc. These contain no white-space or special characters so you could take any of these array items and add as a query parameter to the api call.

### API action: package list to get the list of packages (datasets)

- Include the parameter **'package_list'** in the URL. This action returns the list of datasets / packages provided on the open data portal.
This can be used directly with curl on the command line, in the browser or using Python. 

- `package_list` is added to the end of the url `https://data.gov.ie/api/3/action/`

- In the browser: `https://data.gov.ie/api/3/action/package_list`
- Using Curl on the command line: `curl -i https://data.gov.ie/api/3/action/package_list` 
- Python using `requests` to get the URL as follows:
    `requests.get('https://data.gov.ie/api/3/action/package_list')`

I break this down into the base API action url `https://data.gov.ie/api/3/action/` + 'package_list`
 `response = requests.get(url+'package_list')`


See `dataset_list.py` which uses the requests package to get the data and the json package to work with the json returned from the get request to the Url https://data.gov.ie/api/3/action/package_list
The results key in the json contains a list of packages / datasets. Here are the first few items:
```json
"result": [
        "007-for-population-usually-resident-and-present-in-the-state-by-disability-by-sex-year-and-statistic",
        "011-to-2016-by-composition-of-private-household-age-group-of-youngest-child-censusyear-and-statistic",
        "011-to-2016-number-by-age-group-of-child-children-per-family-unit-type-of-family-unit-and-censusyear",
```


### API action: tag list to get the list of tags.

Similarly to above but adding `action/tag_list` to the URL to get the list of tags.

- In the browser `https://data.gov.ie/api/3/action/tag_list`
- Using Curl: `curl -i https://data.gov.ie/api/3/action/tag_list`
- Python using `requests` to get the URL as follows:
    `requests.get('https://data.gov.ie/api/3/action/tag_list')`

---
## API action: organization_list:

To get the list of organisations that provide datasets on the data.gov.ie open data portal include the parameter 'organization_list' in the URL. This action returns the list of organizations. These organisations are the providers of the datasets. 

- In the browser `https://data.gov.ie/api/3/action/organization_list`
- Using Curl: `curl -i https://data.gov.ie/api/3/action/organization_list`
- Python using `requests` to get the URL as follows:
    `requests.get('https://data.gov.ie/api/3/action/organization_list')`

The Python script uses the `requests` package to get the data and the `json` package to work with the JSON data returned from the `GET` request. The `xlwt` library can then be used to export to an excel worksheet. 

The results key in the json contains a list of organisations. Here are the first few items:
```json
"result": [
        "3d-model-datalyticon",
        "adaptcentre",
        "all-island-research-observatory",
        "an-bord-pleanala",
```

## Calling API with parameters.

You can get a full JSON representation of a dataset, resource or other object by providing some query parameters in the call to the base API URL. 


### API action: organization_show
This API call gives a details of the organization, its status, number of resources, 
packages/datasets, type of datasets and more. The array of "organizations" is returned in the "results" keys of the JSON from the API call to 'https://data.gov.ie/api/3/action/organization_list'.

In Python: In addition to the url, provide the query parameter in a dictionary with the `id` key and value being the organization name returned from call to 'https://data.gov.ie/api/3/action/organization_list'.

You can use some or all of the parameters but the 'id' is required for the organisation name. The id is the organisation name that is returned from the API action: organization_list. For example to get details of the  'all-island-research-observatory':

```python
url = "https://data.gov.ie"
action ="/api/3/action/organization_show"
params = {'id': 'all-island-research-observatory', 'include_users': True, 'include_dataset_count': True, 
          'include_users': True, 'include_groups': True, 'include_tags': True, 'include_datasets': True} 
response = requests.get(url+'/api/3/action/organization_show',params)
```

You can add additional query parameters to get the status of an organization, the number of resources it has, the packages/datasets, types of datasets etc.


In summary:
A request is made with 4 parts to the url:
- the base url ("https://data.gov.ie" + "/api/3/action/" + "organization_show", params)
- where `params` includes the `id` for the organisation and any other combination of params.

params = {'id': 'the_organisations_id', 'include_users': True, 'include_dataset_count': True, 
          'include_users': True, 'include_groups': True, 'include_tags': True, 'include_datasets': True}

---
### API action: package_show
The array of "packages" that is returned from the API call to https://data.gov.ie/api/3/action/package_list is the list of datasets available.

Using the URL `https://data.gov.ie/api/3/action/package_show`

Add the dataset name as the id query parameters after a `?`.

For example, the first dataset in the list returned from the call to https://data.gov.ie/api/3/action/package_list is "007-for-population-usually-resident-and-present-in-the-state-by-disability-by-sex-year-and-statistic".
(Note that this has no white space or special characters that need to be encoded further)


This url can be used in the browser or with curl or Python. (There are no spaces in the string here)
`https://data.gov.ie/api/3/action/package_show?id=007-for-population-usually-resident-and-present-in-the-state-by-disability-by-sex-year-and-statistic`


In Python: as well as the URL, provide the query parameter in a dictionary with the `id` key and value being the dataset name returned from call to 'https://data.gov.ie/api/3/action/package_list'.

```python
url = "https://data.gov.ie"
action ="/api/3/action/package_show"
param={'id':'007-for-population-usually-resident-and-present-in-the-state-by-disability-by-sex-year-and-statistic'}

response = requests.get(url+action,param) 
```
This API action will return details of resources and its formats for a given package id.
The 'resources' is provided in the returned "result" object (from the previous call to "package_show" with the "id").  There may be details of one or more resources. The actual dataset names

For example, the API action call to "`https://data.gov.ie/api/3/action/package_show?id=007-for-population-usually-resident-and-present-in-the-state-by-disability-by-sex-year-and-statistic" will return an array of "resources" within the "results" key. This array contains values for the package_id, format, name, url and many others.

https://data.gov.ie/api/3/action/package_show?id=762c93aa-f821-4ab7-8950-fe86bdf7fd2e
The response from this url is a json file. Pull out the 'result' key from the 'results' array and get the url from here.

See `getdatat.py` getting limerick library data.


### API action: package_show  and tag_show

See [Example API call](https://data.gov.ie/pages/developers).
Get a full JSON representation of a dataset, resource or other object:

- `data.gov.ie/api/3/action/package_show?id=the-walled-towns-of-ireland`

- `data.gov.ie/api/3/action/tag_show?id=marine`

"health and wellbeing"
data.gov.ie/api/3/action/tag_show?id=health%20and%20wellbeing
---
### API action: package_search

Search for packages or resources matching a query. Here using a tag query to get datasets with the tag.

https://data.gov.ie/api/3/action/package_search?=libraries

Here is one results object from the results array. The "resources" array for this item contains a package_id "762c93aa-f821-4ab7-8950-fe86bdf7fd2e" and a url "http://opendata.limerick.ie/opendata/libraries.json"
If you use this url in the browser, this will display the actual dataset. This one is in JSON format.


https://data.gov.ie/api/3/action/package_show?id=762c93aa-f821-4ab7-8950-fe86bdf7fd2e

```json
{
                "license_title": "Creative Commons Attribution 4.0",
                "maintainer": null,
                "issued": "2018-01-05",
                "private": false,
                "maintainer_email": null,
                "num_tags": 2,
                "frequency": "Irregular",
                "id": "762c93aa-f821-4ab7-8950-fe86bdf7fd2e",
                "metadata_created": "2018-01-05T15:26:21.106763",
                "metadata_modified": "2018-03-05T12:20:43.657156",
                "author": null,
                "author_email": null,
                "views": 113,
                "theme": "Education and Sport",
                "state": "active",
                "relationships_as_object": [],
                "creator_user_id": "ef08264c-676d-48c5-aaad-6ce8aa18d521",
                "type": "dataset",
                "resources": [
                    {
                        "cache_last_updated": null,
                        "package_id": "762c93aa-f821-4ab7-8950-fe86bdf7fd2e",
                        "datastore_active": false,
                        "id": "a55efadd-145f-46e1-83bf-e2fed8675abc",
                        "size": null,
                        "state": "active",
                        "api_response_formats": [],
                        "hash": "",
                        "description": "",
                        "format": "GeoJSON",
                        "mimetype_inner": null,
                        "url_type": null,
                        "mimetype": null,
                        "cache_url": null,
                        "name": "Limerick Libraries",
                        "created": "2018-01-05T15:26:21.527646",
                        "url": "http://opendata.limerick.ie/opendata/libraries.json",
                        "notes": "",
                        "api_access_url": "",
                        "last_modified": null,
                        "position": 0,
                        "revision_id": "ef78cac5-742b-44c9-a70a-ee7dc7cb8c85",
                        "resource_type": null,
                        "api_type": ""
                    }
                ],
```
If you use this url in the browser, this will display the actual dataset. This one is in JSON format.

I will try retrieving it using the package_id "762c93aa-f821-4ab7-8950-fe86bdf7fd2e" with the `package_show` api action call.

```python
url = "https://data.gov.ie/"
param = {'id': pkg_id}
pkg_id = "762c93aa-f821-4ab7-8950-fe86bdf7fd2e"
response = requests.get(url+'api/3/action/package_show', param)
results = response.json()
```
https://data.gov.ie/

The dataset is a "resource". The dataset itself can be retreived using the API action `resource_search` with a query parameter.
The same dataset can be extracted using the API action `resource_search` using the package_id as the query parameters.

`https://data.gov.ie/api/3/action/package_show?id=762c93aa-f821-4ab7-8950-fe86bdf7fd2e`

https://data.gov.ie/api/3/action/resource_search?query=id:762c93aa-f821-4ab7-8950-fe86bdf7fd2e

Using two of the functions from the Demo notebooks at the developers corner of data.gov.ie
An example is given here of getting library data and then getting Limerick library data.

- The `package_search(url, query):`function - See `extract_package.py`

    - Search the datasets given query using DGI API:
    - This function returns the meta information about matching package. 
    - Required resource can be selected from the result of below funtion 
    - Search Query: "libraries"

    - From the result of the package_search function, you can get the package_id

- The `extract_pkg_data(url, pkg_id, resc_arr_ind)` function. See `extract_package.py`
- Function to extract data from DGI API:

- From the result of the `package_search` function above, you can get the package_id
 
    * `id` - is the `package_id` and 
    * `resc_arr_ind` - is the array index of the resources that need to be extracted. In the Limerick library example this is 0.

Note I am only looking at the functions in the notebooks to figure out how to use the APIs.
I am not doing anything elaborate with the data for now.

---
My own trial and error
See `libraries.py` file
I think the query could be anything from the tags I downloaded into tag_list.json
```python
import requests
import json
url = 'https://data.gov.ie/'
query = "libraries"
response = requests.get(url+'api/3/action/package_search', {'q':query})
print(response.status_code)

results = response.json()
print("writing the returned JSON to an json file")
filename = 'libraries.json'
if filename:
    # write the json data
    with open(filename, 'w') as f:
        json.dump(results, f, indent=4)

```

This here gives me the json relating to libraries.
Can look into the json and see the ids

```json
{
                "license_title": "Creative Commons Attribution 4.0",
                "maintainer": null,
                "issued": "2018-01-05",
                "private": false,
                "maintainer_email": null,
                "num_tags": 2,
                "frequency": "Irregular",
                "id": "762c93aa-f821-4ab7-8950-fe86bdf7fd2e",
                "metadata_created": "2018-01-05T15:26:21.106763",
                "metadata_modified": "2018-03-05T12:20:43.657156",
                "author": null,
                "author_email": null,
                "views": 108,
                "theme": "Education and Sport",
                "state": "active",
                "relationships_as_object": [],
                "creator_user_id": "ef08264c-676d-48c5-aaad-6ce8aa18d521",
                "type": "dataset",
                "resources": [
```

```python
param = {'id': pkg_id}
url =''https://data.gov.ie/'
pkg_id:'762c93aa-f821-4ab7-8950-fe86bdf7fd2e'
response = requests.get(url+'api/3/action/package_show', param)
results = response.json()
```
---

https://data.gov.ie/api/3/action/package_show?id=aasleagh-hse-rainfall-data
"aasleagh-hse-rainfall-data"

https://data.gov.ie/api/3/action/package_show?id=railway-stations-osi-national-250k-map-of-ireland


a package from the list of packages
visits-to-and-from-ireland-by-year-reason-for-journey-and-statistic

data.gov.ie/api/3/action/resource_search?query=name:visits-to-and-from-ireland-by-year-reason-for-journey-and-statistic