"""
# API Client for Submittable.com

This module is designed to provide easy Python access to the API provided by
https://submittable.com. Additional information about this API can be found at
https://apidoc.submittable.com.

Requires existence of Python requests module:
http://docs.python-requests.org/

"""
from datetime import datetime
import time

try:
    import requests
except ImportError:
    print """
            Error - You must have the ``requests`` module installed in your
            Python path.
          """

BASE_API_URI = "https://api.submittable.com/v1/"
CATEGORIES_URI = "categories/"
ORGANIZATION_URI = "organization/"  # This is currently not implemented due to
STAFF_URI = "staff/"                # issues with these endpoints FIXME
PAYMENTS_URI = "payments/"
SUBMISSIONS_URI = "submissions/"
SUBMITTERS_URI = "submitters/"

ALLOWED_SORTS = [
    'submitted',
    'category',
    'submitter',
]

ALLOWED_DIRECTIONS = [
    'desc',
    'asc'
]

MAX_API_COUNT = 200

ALLOWED_STATUSES = [
    'inprogress',
    'accepted',
    'declined',
    'completed',
    'withdrawn',
]


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
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(response)

    def category(self, cat_id=None):
        """ Returns information about a single Category."""
        if not cat_id:
            raise Exception('No Category ID specified.')

        query_uri = "%s%s%s" % (BASE_API_URI, CATEGORIES_URI, cat_id)
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(response)

    def category_form(self, cat_id=None):
        """ Returns the form info associated with the Category."""
        if not cat_id:
            raise Exception('No Category ID specified.')

        query_uri = "%s%s%sform/" % (BASE_API_URI, CATEGORIES_URI, cat_id)
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(response)

    def category_submitters(self, cat_id=None, page=None, per_page=None):
        """ Returns user records that have submitted this form. """
        if not cat_id:
            raise Exception('No Category ID specified.')
        per_page = per_page or self.per_page
        page = page or self.start_page

        query_uri = "%s%s%ssubmitters/?page=%s&count=%s" % (
            BASE_API_URI,
            CATEGORIES_URI,
            cat_id,
            page,
            per_page,
        )
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(response)

    def submissions(self, sort='submitted', direction='desc', page=1,
                    per_page=20, status='inprogress'):
        """
        Returns a list of Submissions. Allows pagination, sorting and filters.
        """
        if not sort in ALLOWED_SORTS:
            raise Exception('Sort value not found: %s' % sort)

        if not direction in ALLOWED_DIRECTIONS:
            raise Exception('Direction value not found: %s' % direction)

        if not status in ALLOWED_STATUSES:
            raise Exception('Status value not found: %s' % status)

        if per_page > 200:
            print """
                Exceeded max per_page allowance per API restrictions.
                Set per_page value to max of 200.
                """
            per_page = 200

        query_uri = "%s%s?sort=%s&dir=%s&page=%s&count=%s&status=%s" % (
            BASE_API_URI,
            SUBMISSIONS_URI,
            sort,
            direction,
            page,
            per_page,
            status,
        )
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(response)

    def submission(self, sub_id=None):
        """ Returns information about a single Submission."""
        if not sub_id:
            raise Exception('No Submission ID specified.')

        query_uri = "%s%s%s" % (BASE_API_URI, SUBMISSIONS_URI, sub_id)
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(response)

    def submission_labels(self, sub_id=None):
        """ Returns labels for a single Submission."""
        if not sub_id:
            raise Exception('No Submission ID specified.')

        query_uri = "%s%s%s/labels" % (BASE_API_URI, SUBMISSIONS_URI, sub_id)
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(response)

    def submission_history(self, sub_id=None):
        """ Returns history for a single Submission."""
        if not sub_id:
            raise Exception('No Submission ID specified.')

        query_uri = "%s%s%s/history" % (BASE_API_URI, SUBMISSIONS_URI, sub_id)
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(response)

    def submission_file(self, sub_id=None, file_guid=None):
        """ Returns a File attached to a single Submission."""
        if not sub_id:
            raise Exception('No Submission ID specified.')
        if not file_guid:
            raise Exception('No GUID specified.')

        query_uri = "%s%s%s/file/%s" % (
            BASE_API_URI,
            SUBMISSIONS_URI,
            sub_id,
            file_guid
        )
        print query_uri
        return requests.get(query_uri, auth=(self.username, self.apitoken))

    def submission_form(self, sub_id=None):
        """ Returns Form attached to a single Submission."""
        if not sub_id:
            raise Exception('No Submission ID specified.')

        query_uri = "%s%s%s/form" % (BASE_API_URI, SUBMISSIONS_URI, sub_id)
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(response)

    def submission_assignments(self, sub_id=None):
        """ Returns Assignments attached to a single Submission."""
        if not sub_id:
            raise Exception('No Submission ID specified.')

        query_uri = "%s%s%s/assignments" % (
            BASE_API_URI,
            SUBMISSIONS_URI,
            sub_id
        )
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(response)

    def payments(self, year=None, month=None):
        """ Returns Assignments attached to a single Submission."""
        if not year:
            raise Exception('No Year specified.')
        if not month:
            raise Exception('No Month specified.')

        query_uri = "%s%s%s/%s" % (BASE_API_URI, PAYMENTS_URI, year, month)
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(response)

    def submitters(self, page=1, per_page=20):
        """ Returns Submitters for an Organization."""
        query_uri = "%s%s?page=%s&count=%s" % (
            BASE_API_URI,
            SUBMITTERS_URI,
            page,
            per_page
        )
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(response)


class SubmittableAPIResponse():
    """
    The response object from the Submittable API. Expects reponse from requests
    module.
    """

    def __init__(self, response=None):
        if not response:
            raise Exception("Error in Response")
        self.data = response.json()
        # Common fields returned by generally everything
        self.current_page = self.data.get('current_page', 0)
        self.total_pages = self.data.get('total_pages', )
        self.total_items = self.data.get('total_items', None)
        self.count = self.data.get('count', len(self.data.get('items', [])))
        self.items_per_page = self.data.get('items_per_page', 20)
        self.url = self.data.get('url', '')
        self.type = self.data.get('type', None)

        # Fields specific to different object types
        # Specific Category
        self.form_url = self.data.get('form_url', '')
        self.category_id = self.data.get('category_id', 0)
        self.name = self.data.get('name', '')
        self.description = self.data.get('description', '')
        self.blind_level = self.data.get('blind_level', 0)
        self.blind_value = self.data.get('blind_value', 0)
        self.start_date = self.data.get('start_date', None)
        self.expire_date = self.data.get('expire_date', None)
        self.active = self.data.get('active', False)
        self.order = self.data.get('order', 0)
        self.formfields = self.data.get('formfields', [])
        # Specific Submission
        self.submission_id = self.data.get('submission_id', 0)
        self.submission_time_created = time.strptime(
            self.data.get('date_created', "2014-05-21T11:58:57"),
            "%Y-%m-%dT%I:%M:%S"
        )
        self.submission_date_created = datetime.fromtimestamp(
            time.mktime(self.submission_time_created)
        )
        self.title = self.data.get('title', 'UNTITLED')
        self.file_id = self.data.get('file_id', 0)
        self.status = self.data.get('status')
        self.is_archived = self.data.get('is_archived')
        self.category = self.data.get('category', {})
        self.submitter = self.data.get('submitter', {})
        self.payment = self.data.get('payment', {})
        self.votes = self.data.get('votes', {})
        self.assignments = self.data.get('assignments', {})
        self.labels = self.data.get('labels', {})
        self.form = self.data.get('form', {})
        self.files = self.data.get('files', [])
        # Specific Payment
        self.payment_id = self.data.get('payment_id', 0)
        self.payment_time_created = time.strptime(
            self.data.get('payment_date', "2014-05-21T11:58:57"),
            "%Y-%m-%dT%I:%M:%S"
        )
        self.payment_date_created = datetime.fromtimestamp(
            time.mktime(self.payment_time_created)
        )
        self.payment_amount = self.data.get('amount', 0.00)
        self.payment_fee = self.data.get('fee', 0.00)
        self.payment_refunded = self.data.get('refunded')
        # Items themselves
        self.items = self.data.get('items', [])
