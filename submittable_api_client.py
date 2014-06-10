"""
This module is designed to provide easy Python access to the API provided by
https://submittable.com. Additional information about this API can be found at
https://apidoc.submittable.com.

Requires existence of Python requests module:
http://docs.python-requests.org/

.. moduleauthor:: Shawn Rider <shawn@shawnrider.com>

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

    :param username: Submittable.com username
    :type username: str
    :param apitoken: Submittable.com API token
    :type apitoken: str
    :param per_page: Per page item limit (defaults to 20)
    :type per_page: int

    :returns: :class:`SubmittableAPIResponse` containing a list of content-specific
        objects and related metadata.
    """

    def __init__(self, username=None, apitoken=None, per_page=20):
        if not username or not apitoken:
            raise Exception('No username/apitoken credentials supplied.')
        self.username = username
        self.apitoken = apitoken
        self.per_page = 20
        self.start_page = 1

    def categories(self):
        """
        Returns a list of Categories. Allows no pagination.

        :returns: :class:`SubmittableAPIResponse` containing a list of content-specific
            objects and related metadata.
        """

        query_uri = "%s%s" % (BASE_API_URI, CATEGORIES_URI)
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(response=response, obj_type='categories')

    def category(self, cat_id=None):
        """
        Returns information about a single Category.

        :param cat_id: ID of Category
        :type cat_id: int

        :returns: :class:`SubmittableAPIResponse` containing a list of content-specific
            objects and related metadata.
        """
        if not cat_id:
            raise Exception('No Category ID specified.')

        query_uri = "%s%s%s" % (BASE_API_URI, CATEGORIES_URI, cat_id)
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(response=response, obj_type='category')

    def category_form(self, cat_id=None):
        """
        Returns the form info associated with the Category.

        :param cat_id: ID of Category
        :type cat_id: int

        :returns: :class:`SubmittableAPIResponse` containing a list of content-specific
            objects and related metadata.
        """
        if not cat_id:
            raise Exception('No Category ID specified.')

        query_uri = "%s%s%sform/" % (BASE_API_URI, CATEGORIES_URI, cat_id)
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(response=response, obj_type='category_form')

    def category_submitters(self, cat_id=None, page=None, per_page=None):
        """
        Returns user records that have submitted this form.

        :param cat_id: ID of Category
        :type cat_id: int
        :param page: Page number to start on.
        :type page: int
        :param per_page: Number of items per page to return.
        :type per_page: int

        :returns: :class:`SubmittableAPIResponse` containing a list of content-specific
            objects and related metadata.
        """
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

        return SubmittableAPIResponse(response=response, obj_type='category_submitters')

    def submissions(self, sort='submitted', direction='desc', page=1,
                    per_page=20, status='inprogress'):
        """
        Returns a list of Submissions. Allows pagination, sorting and filters.

        :param sort: Keyword for attribute to sort against.
        :type sort: str
        :param direction: Keyword for direction of sort (asc or desc).
        :type direction: str
        :param page: Page number to start on.
        :type page: int
        :param per_page: Number of items per page to return.
        :type per_page: int
        :param status: Keyword for Status value to filter against.
        :type status: str

        :returns: :class:`SubmittableAPIResponse` containing a list of content-specific
            objects and related metadata.
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

        return SubmittableAPIResponse(response, 'submissions')

    def submission(self, sub_id=None):
        """
        Returns information about a single Submission.

        :param sub_id: ID of Submission object to retrieve.
        :type sub_id: int

        :returns: :class:`SubmittableAPIResponse` containing a list of content-specific
            objects and related metadata.
        """
        if not sub_id:
            raise Exception('No Submission ID specified.')

        query_uri = "%s%s%s" % (BASE_API_URI, SUBMISSIONS_URI, sub_id)
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(response=response, obj_type='submission')

    def submission_labels(self, sub_id=None):
        """
        Returns labels for a single Submission.

        :param sub_id: ID of Submission object to retrieve.
        :type sub_id: int

        :returns: :class:`SubmittableAPIResponse` containing a list of content-specific
            objects and related metadata.
        """
        if not sub_id:
            raise Exception('No Submission ID specified.')

        query_uri = "%s%s%s/labels" % (BASE_API_URI, SUBMISSIONS_URI, sub_id)
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(response=response, obj_type='submission_labels')

    def submission_history(self, sub_id=None):
        """
        Returns history for a single Submission.

        :param sub_id: ID of Submission object to retrieve.
        :type sub_id: int

        :returns: :class:`SubmittableAPIResponse` containing a list of content-specific
            objects and related metadata.
        """
        if not sub_id:
            raise Exception('No Submission ID specified.')

        query_uri = "%s%s%s/history" % (BASE_API_URI, SUBMISSIONS_URI, sub_id)
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(response=response, obj_type='submission_history')

    def submission_file(self, sub_id=None, file_guid=None):
        """
        Returns a File attached to a single Submission.

        :param sub_id: ID of Submission object to retrieve.
        :type sub_id: int
        :param file_guid: GUID for File object attached to Submission object.
        :type file_guid: str

        :returns: :class:`SubmittableAPIResponse` containing a list of content-specific
            objects and related metadata.
        """
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
        """
        Returns Form attached to a single Submission.

        :param sub_id: ID of Submission object to retrieve.
        :type sub_id: int

        :returns: :class:`SubmittableAPIResponse` containing a list of content-specific
            objects and related metadata.
        """
        if not sub_id:
            raise Exception('No Submission ID specified.')

        query_uri = "%s%s%s/form" % (BASE_API_URI, SUBMISSIONS_URI, sub_id)
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(response=response, obj_type='submission_form')

    def submission_assignments(self, sub_id=None):
        """
        Returns Assignments attached to a single Submission.

        :param sub_id: ID of Submission object to retrieve.
        :type sub_id: int

        :returns: :class:`SubmittableAPIResponse` containing a list of content-specific
            objects and related metadata
        """
        if not sub_id:
            raise Exception('No Submission ID specified.')

        query_uri = "%s%s%s/assignments" % (
            BASE_API_URI,
            SUBMISSIONS_URI,
            sub_id
        )
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(response=response, obj_type='submission_assignments')

    def payments(self, year=None, month=None):
        """
        Returns Assignments attached to a single Submission.

        :param year: Year (YYYY) value to filter against.
        :type year: int
        :param month: Numeric month (MM) value to filter against.
        :type month: int

        :returns: :class:`SubmittableAPIResponse` containing a list of content-specific
            objects and related metadata.
        """
        if not year:
            raise Exception('No Year specified.')
        if not month:
            raise Exception('No Month specified.')

        query_uri = "%s%s%s/%s" % (BASE_API_URI, PAYMENTS_URI, year, month)
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(response=response, obj_type='payments')

    def submitters(self, page=1, per_page=20):
        """
        Returns Submitters for an Organization.

        :param page: Page number to start on.
        :type page: int
        :param per_page: Number of items per page to return.
        :type per_page: int

        :returns: :class:`SubmittableAPIResponse` containing a list of content-specific
            objects and related metadata.
        """
        query_uri = "%s%s?page=%s&count=%s" % (
            BASE_API_URI,
            SUBMITTERS_URI,
            page,
            per_page
        )
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(response=response, obj_type='submitters')


class SubmittableAPIResponse():
    """
    The response object from the Submittable API. Expects reponse from requests
    module.

    :param response: Response object from ``requests`` module.
    :type response: obj
    :param obj_type: String keyword for type of object being requested.
    :type obj_type: str

    :returns: None
    """

    def __init__(self, response=None, obj_type=None):
        if not response:
            raise Exception("Error in Response")
        self.data = response.json()
        # Common fields returned by generally everything
        self.current_page = self.data.get('current_page', 0)
        self.total_pages = self.data.get('total_pages', 0)
        self.total_items = self.data.get(
            'total_items', len(self.data.get('items', [])))
        self.count = self.data.get('count', len(self.data.get('items', [])))
        self.items_per_page = self.data.get('items_per_page', 20)
        self.url = self.data.get('url', '')
        self.type = self.data.get('type', None)

        # Initialize items listing
        self.items = []

        if obj_type == 'category':
            self.provision_category()
        elif obj_type == 'categories':
            self.provision_categories(self.data['items'])
        elif obj_type == 'category_form':
            self.provision_category_form()
        elif obj_type == 'category_submitters':
            self.provision_category_submitters(self.data['items'])
        elif obj_type == 'submission':
            self.provision_submission()
        elif obj_type == 'submissions':
            self.provision_submissions(self.data['items'])
        elif obj_type == 'submission_assignments':
            self.provision_submission_assignments(self.data['items'])
        elif obj_type == 'submission_history':
            self.provision_submission_history(self.data['items'])
        elif obj_type == 'submission_labels':
            self.provision_submission_labels(self.data['items'])
        elif obj_type == 'submission_form':
            self.provision_submission_form()
        elif obj_type == 'payments':
            self.provision_payments(self.data['items'])
        elif obj_type == 'submitters':
            self.provision_submitters(self.data['items'])
        else:
            raise Exception(
                "Object type not recognized: %s" % obj_type
            )

    def provision_category(self):
        """ Build Category-specific metadata and item objects. """
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

    def provision_categories(self, cat_data):
        """ Build Category-specific metadata and item objects. """
        for cat_data in self.data.get('items', []):
            self.items.append(Category(cat_data))

    def provision_submission(self, submission_data):
        """ Build Submission-specific metadata and item objects. """
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

    def provision_payments(self, pay_data):
        """ Build Payment-specific metadata and item objects. """
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

    def provision_submitters(self, submitter_data):
        """ Build Submitter-specific metadata and item objects. """
        pass


class Category():
    """
    Item object container for Categories.

    :param data: Data dictionary in JSON format.
    :type data: str

    :returns: None
    """
    def __init__(self, data):
        self.form_url = data.get('form_url', '')
        self.category_id = data.get('category_id', 0)
        self.name = data.get('name', '')
        self.description = data.get('description', '')
        self.blind_level = data.get('blind_level', 0)
        self.blind_value = data.get('blind_value', 0)
        self.start_date = data.get('start_date', None)
        self.expire_date = data.get('expire_date', None)
        self.active = data.get('active', False)
        self.order = data.get('order', 0)
        self.formfields = data.get('formfields', [])
