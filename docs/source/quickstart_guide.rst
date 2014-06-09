Quickstart Guide
================
This library generally installs and works like many others.

Installation
------------
Install the library via pip::

    pip install submittable_api_client

Basic Usage
-----------
Load up an API client with credentials::

    In [1]: from submittable_api_client import SubmittableAPIClient
    In [2]: client = SubmittableAPIClient(username='you@example.com', apitoken='555')

Note: you will need to use your own Submittable.com username and API Token.

Once the client is created it can be used to make multiple calls to the
Submittable.com API. Here are some examples of the calls that can be made::

    In [3]: cats = client.categories()
    https://api.submittable.com/v1/categories/
    In [4]: cats.count
    Out[4]: 2
    In [5]: cats.items
    Out[5]:
    [{u'active': True, ... }, ...]

API Endpoints
-------------
The following API endpoints are available through this client.

* Categories
* Submissions
* Payments
* Submitters

Each one supports the sorting/filtering parameters made available by
Submittable.com
