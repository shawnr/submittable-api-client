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

    In [4]: dir(cats)
    Out[4]:
    ['__doc__',
     '__init__',
     '__module__',
     'count',
     'current_page',
     'data',
     'items',
     'items_per_page',
     'provision_categories',
     'provision_category',
     'provision_category_form',
     'provision_category_submitters',
     'provision_payments',
     'provision_submission',
     'provision_submission_assignments',
     'provision_submission_form',
     'provision_submission_history',
     'provision_submission_labels',
     'provision_submissions',
     'provision_submitters',
     'total_items',
     'total_pages',
     'type',
     'url']

    In [5]: cats.count
    Out[5]: 2

    In [6]: for item in cats.items:
       ...:     print item.name
       ...:
    Category One Name
    Second Category Name

    In [7]: dir(cats.items[0])
    Out[7]:
    ['__doc__',
     '__init__',
     '__module__',
     'active',
     'blind_level',
     'blind_value',
     'category_id',
     'description',
     'expire_date',
     'form_url',
     'formfields',
     'name',
     'order',
     'start_date']

API Endpoints
-------------
The following API endpoints are available through this client.

* Categories
* Submissions
* Payments
* Submitters

Each one supports the sorting/filtering parameters made available by
Submittable.com.
