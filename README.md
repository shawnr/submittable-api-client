Submittable API Client
======================

A Python client for the Submittable.com REST API.

Submittable.com is a service that allows you to post application and
submission forms for users to fill in. They allow you to collect payments
for submissions, assign staff to review submissions, and generally provide
the needed workflow for accepting applications or submissions for your
organization.

This API client is designed to leverage the Submittable REST API via Python
scripts for various tasks and management duties. The API provided by
Submittable.com is currently read-only, so this client does not cover creating
any data.

Supported API Calls
-------------------
Currently supported API calls are:

* Categories
* Submissions
* Payments
* Submitters

There are currently API endpoints in place for Organization and Staff, but these
endpoints are problematic at this time (they are returning server errors). They
will be revisited when functionality returns and time allows.

Requirements
------------
This module is currently written for Python 2.7*. It requires the ``requests``
module available here: http://docs.python-requests.org/

Usage
-----
Directions forthcoming.
