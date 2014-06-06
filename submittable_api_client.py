"""
# API Client for Submittable.com

This module is designed to provide easy Python access to the API provided by
https://submittable.com. Additional information about this API can be found at
https://apidoc.submittable.com.

Requires existence of Python requests module:
http://docs.python-requests.org/

"""
try:
    import requests
except ImportError:
    print """
            Error - You must have the ``requests`` module installed in your
            Python path.
          """

BASE_API_URI = "https://api.submittable.com/v1/"
CATEGORIES_URI = "categories/"
ORGANIZATION_URI = "organization/" # This is currently not implemented due to
STAFF_URI = "staff/"               # issues with this endpoint
PAYMENTS_URI = "payments/"
SUBMISSIONS_URI = "submissions/"
SUBMITTERS_URI = "submitters/"

class SubmittableAPIClient():
    """
    The primary class instantiated to make an API call.
    """

    def __init__(self, username=None, apitoken=None, per_page=20):
        if not username or not apitoken:
            raise Exception('No username/apitoken credentials supplied.')
        self.username = username
        self.apitoken = apitoken
        self.per_page = 20
        self.start_page = 1

    def categories(self):
        """Returns a list of Categories. Allows no pagination."""

        query_uri = "%s%s" % (BASE_API_URI, CATEGORIES_URI)
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(response)

    def category(self, cat_id=None):
        """ Returns information about a single Category."""
        if not cat_id:
            raise Exception('No Category ID specified.')

        query_uri = "%s%s%s" % (BASE_API_URI, CATEGORIES_URI, cat_id)
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(response)


    def category_form(self, cat_id=None, page=None, per_page=None):
        """ Returns the form info associated with the Category."""
        if not cat_id:
            raise Exception('No Category ID specified.')
        page = page or self.start_page
        per_page = per_page or self.per_page


    def category_submitters(self, cat_id=None, page=None, per_page=None):
        """ Returns user records that have submitted this form. """
        if not cat_id:
            raise Exception('No Category ID specified.')
        per_page = per_page or self.per_page
        per_page = per_page or self.per_page


class SubmittableAPIResponse():
    """
    The response object from the Submittable API. Expects reponse from requests
    module.
    """

    def __init__(self, response=None):
        if not response:
            raise Exception('No response supplied.')
        data = response.json()
        self.current_page = data.get('current_page', None)
        self.total_pages = data.get('total_pages', None)
        self.total_items = data.get('total_items') or data.get('count') or len(data.get('items'))
        self.items_per_page = data.get('items_per_page', None)
        self.url = data.get('url', None)
        self.items = data.get('items', [])

