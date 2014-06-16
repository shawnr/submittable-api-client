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

import requests

# Prevent import * from importing all our "local" globals and imports.
__all__ = (
    'Assignment', 'AssignmentsContainer', 'Category', 'File',
    'FormFieldContainer', 'FormFieldItem', 'LabelsContainer',
    'Payment', 'Submission', 'SubmissionHistory', 'SubmissionLabel',
    'SubmittableAPIClient', 'SubmittableAPIResponse', 'SubmittedFormContainer',
    'SubmittedFormField', 'Submitter', 'Votes',
)

BASE_API_URI = "https://api.submittable.com/v1/"
CATEGORIES_URI = "categories/"
ORGANIZATION_URI = "organization/"  # This is currently not implemented due to
STAFF_URI = "staff/"                # issues with these endpoints FIXME
PAYMENTS_URI = "payments/"
SUBMISSIONS_URI = "submissions/"
SUBMITTERS_URI = "submitters/"

ALLOWED_SORTS = (
    'submitted',
    'category',
    'submitter',
)

ALLOWED_DIRECTIONS = (
    'desc',
    'asc'
)

MAX_API_COUNT = 200

ALLOWED_STATUSES = (
    'inprogress',
    'accepted',
    'declined',
    'completed',
    'withdrawn',
)


class SubmittableAPIClient(object):
    """
    The primary class instantiated to make an API call.

    :param username: Submittable.com username
    :type username: str
    :param apitoken: Submittable.com API token
    :type apitoken: str
    :param per_page: Per page item limit (defaults to 20)
    :type per_page: int

    :returns: :class:`SubmittableAPIResponse` containing a list of
        content-specific objects and related metadata.
    """

    def __init__(self, username=None, apitoken=None, per_page=20):
        if not username or not apitoken:
            raise Exception('No username/apitoken credentials supplied.')
        self.username = username
        self.apitoken = apitoken
        self.per_page = per_page
        self.start_page = 1

    def categories(self):
        """
        Returns a list of Categories. Allows no pagination.

        :returns: :class:`SubmittableAPIResponse` containing a list of
            content-specific objects and related metadata.
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

        :returns: :class:`SubmittableAPIResponse` containing a list of
            content-specific objects and related metadata.
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

        :returns: :class:`SubmittableAPIResponse` containing a list of
            content-specific objects and related metadata.
        """
        if not cat_id:
            raise Exception('No Category ID specified.')

        query_uri = "%s%s%sform/" % (BASE_API_URI, CATEGORIES_URI, cat_id)
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(
            response=response, obj_type='category_form')

    def category_submitters(self, cat_id=None, page=None, per_page=None):
        """
        Returns user records that have submitted this form.

        :param cat_id: ID of Category
        :type cat_id: int
        :param page: Page number to start on.
        :type page: int
        :param per_page: Number of items per page to return.
        :type per_page: int

        :returns: :class:`SubmittableAPIResponse` containing a list of
            content-specific objects and related metadata.
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

        return SubmittableAPIResponse(
            response=response, obj_type='category_submitters'
        )

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

        :returns: :class:`SubmittableAPIResponse` containing a list of
            content-specific objects and related metadata.
        """
        if sort not in ALLOWED_SORTS:
            raise Exception('Sort value not found: %s' % sort)

        if direction not in ALLOWED_DIRECTIONS:
            raise Exception('Direction value not found: %s' % direction)

        if status not in ALLOWED_STATUSES:
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

        :returns: :class:`SubmittableAPIResponse` containing a list of
            content-specific objects and related metadata.
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

        :returns: :class:`SubmittableAPIResponse` containing a list of
            content-specific objects and related metadata.
        """
        if not sub_id:
            raise Exception('No Submission ID specified.')

        query_uri = "%s%s%s/labels" % (BASE_API_URI, SUBMISSIONS_URI, sub_id)
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(
            response=response, obj_type='submission_labels')

    def submission_history(self, sub_id=None):
        """
        Returns history for a single Submission.

        :param sub_id: ID of Submission object to retrieve.
        :type sub_id: int

        :returns: :class:`SubmittableAPIResponse` containing a list of
            content-specific objects and related metadata.
        """
        if not sub_id:
            raise Exception('No Submission ID specified.')

        query_uri = "%s%s%s/history" % (BASE_API_URI, SUBMISSIONS_URI, sub_id)
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(
            response=response, obj_type='submission_history')

    def submission_file(self, sub_id=None, file_guid=None):
        """
        Returns a File attached to a single Submission.

        :param sub_id: ID of Submission object to retrieve.
        :type sub_id: int
        :param file_guid: GUID for File object attached to Submission object.
        :type file_guid: str

        :returns: :class:`SubmittableAPIResponse` containing a list of
            content-specific objects and related metadata.
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

        :returns: :class:`SubmittableAPIResponse` containing a list of
            content-specific objects and related metadata.
        """
        if not sub_id:
            raise Exception('No Submission ID specified.')

        query_uri = "%s%s%s/form" % (BASE_API_URI, SUBMISSIONS_URI, sub_id)
        print query_uri
        response = requests.get(query_uri, auth=(self.username, self.apitoken))

        return SubmittableAPIResponse(
            response=response, obj_type='submission_form')

    def submission_assignments(self, sub_id=None):
        """
        Returns Assignments attached to a single Submission.

        :param sub_id: ID of Submission object to retrieve.
        :type sub_id: int

        :returns: :class:`SubmittableAPIResponse` containing a list of
            content-specific objects and related metadata
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

        return SubmittableAPIResponse(
            response=response, obj_type='submission_assignments')

    def payments(self, year=None, month=None):
        """
        Returns Assignments attached to a single Submission.

        :param year: Year (YYYY) value to filter against.
        :type year: int
        :param month: Numeric month (MM) value to filter against.
        :type month: int

        :returns: :class:`SubmittableAPIResponse` containing a list of
            content-specific objects and related metadata.
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

        :returns: :class:`SubmittableAPIResponse` containing a list of
            content-specific objects and related metadata.
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


class SubmittableAPIResponse(object):
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
        self.submission_id = 0
        self.labels = {}
        self.blind_level = 0
        self.blind_value = 0
        self.file_id = 0
        self.time_created = None
        self.files = []
        self.votes = {}
        self.payment = {}
        self.submitter = {}
        self.category = {}
        self.title = 'UNTITLED'
        self.start_date = None
        self.expire_date = None
        self.date_created = None
        self.status = ''
        self.form_url = ''
        self.category_id = 0
        self.assignments = None

        # Initialize items listing
        self.items = []

        if obj_type == 'category':
            self.provision_category()
        elif obj_type == 'categories':
            self.provision_categories()
        elif obj_type == 'category_form':
            self.provision_category_form()
        elif obj_type == 'category_submitters':
            self.provision_category_submitters()
        elif obj_type == 'submission':
            self.provision_submission()
        elif obj_type == 'submissions':
            self.provision_submissions()
        elif obj_type == 'submission_assignments':
            self.provision_submission_assignments()
        elif obj_type == 'submission_history':
            self.provision_submission_history()
        elif obj_type == 'submission_labels':
            self.provision_submission_labels()
        elif obj_type == 'submission_form':
            self.provision_submission_form()
        elif obj_type == 'payments':
            self.provision_payments()
        elif obj_type == 'submitters':
            self.provision_submitters()
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
        # TODO: do these return KeyError, None, or '' if no value?
        # Maybe use try/except.
        self.start_date = self.data.get('start_date', None)
        self.expire_date = self.data.get('expire_date', None)
        self.active = self.data.get('active', False)
        self.order = self.data.get('order', 0)
        self.formfields = FormFieldContainer(self.data.get('formfields', {}))

    def provision_category_form(self):
        """ Build category form objects. """
        for data in self.data.get('items', []):
            self.items.append(FormFieldItem(data))

    def provision_category_submitters(self):
        """ Build category form objects. """
        for data in self.data.get('items', []):
            self.items.append(Submitter(data))

    def provision_categories(self):
        """ Build Category-specific metadata and item objects. """
        for data in self.data.get('items', []):
            self.items.append(Category(data))

    def provision_submission_assignments(self):
        """ Build Assignment-specific metadata and item objects. """
        for data in self.data.get('items', []):
            self.items.append(Assignment(data))

    def provision_submission_form(self):
        """ Build submitted form-specific metadata and item objects. """
        for data in self.data.get('items', []):
            self.items.append(SubmittedFormField(data))

    def provision_submission_history(self):
        """ Build submission history metadata and item objects. """
        for data in self.data.get('items', []):
            self.items.append(SubmissionHistory(data))

    def provision_submission_labels(self):
        """ Build submission label metadata and item objects. """
        for data in self.data.get('items', []):
            self.items.append(SubmissionLabel(data))

    def provision_submission(self):
        """ Build Submission-specific metadata and item objects. """
        self.submission_id = self.data.get('submission_id', 0)
        self.time_created = time.strptime(
            self.data.get('date_created', "2014-05-21T11:58:57"),
            "%Y-%m-%dT%I:%M:%S"
        )
        self.date_created = datetime.fromtimestamp(
            time.mktime(self.time_created)
        )
        # TODO: find out if no data will cause a KeyError or
        # "falsy" value, then consider try/except KeyError.
        self.title = self.data.get('title', 'UNTITLED')
        self.file_id = self.data.get('file_id', 0)
        self.status = self.data.get('status', '')
        self.is_archived = self.data.get('is_archived', False)
        self.category = Category(self.data.get('category', {}))
        self.submitter = Submitter(self.data.get('submitter', {}))
        self.payment = Payment(self.data.get('payment', {}))
        self.votes = Votes(self.data.get('votes', {}))
        self.assignments = AssignmentsContainer(
            self.data.get('assignments', {}))
        self.labels = LabelsContainer(self.data.get('labels', {}))
        self.form = SubmittedFormContainer(self.data.get('form', {}))
        for data in self.data.get('files'):
            self.files.append(File(data))

    def provision_submissions(self):
        """ Build submission listing metadata and item objects. """
        for data in self.data.get('items', []):
            self.items.append(Submission(data))

    def provision_payments(self):
        """ Build Payment-specific metadata and item objects. """
        for data in self.data.get('items', []):
            self.items.append(Payment(data))

    def provision_submitters(self):
        """ Build Submitter-specific metadata and item objects. """
        for data in self.data.get('items', []):
            self.items.append(Submitter(data))


class Payment(object):
    """
    Representation of Payment as a Python object.

    :param data: Data dictionary in JSON format.
    :type data: str
    """
    def __init__(self, data):
        self.payment_id = data.get('payment_id', 0)
        self.time_created = time.strptime(
            data.get('payment_date', "2014-05-21T11:58:57"),
            "%Y-%m-%dT%I:%M:%S"
        )
        self.payment_date = datetime.fromtimestamp(
            time.mktime(self.time_created)
        )
        self.amount = data.get('amount', 0.00)
        self.fee = data.get('fee', 0.00)
        self.refunded = data.get('refunded', False)
        self.category_id = data.get('category_id', 0)
        self.submission_id = data.get('submission_id', 0)
        self.description = data.get('description', '')
        self.settled = data.get('settled', False)
        self.submitter = Submitter(data.get('submitter', {}))


class Submission(object):
    """
    Representation of Submission as a Python object.

    :param data: Data dictionary in JSON format.
    :type data: str
    """
    def __init__(self, data):
        self.submission_id = data.get('submission_id', 0)
        self.time_created = time.strptime(
            data.get('date_created', "2014-05-21T11:58:57"),
            "%Y-%m-%dT%I:%M:%S"
        )
        self.date_created = datetime.fromtimestamp(
            time.mktime(self.time_created)
        )
        self.title = data.get('title', 'UNTITLED')
        self.file_id = data.get('file_id', 0)
        self.status = data.get('status', '')
        self.is_archived = data.get('is_archived', False)
        self.category = Category(data.get('category', {}))
        self.submitter = Submitter(data.get('submitter', {}))
        if data.get('payment'):
            self.payment = Payment(data.get('payment', {}))
        else:
            self.payment = None
        if data.get('votes'):
            self.votes = Votes(data.get('votes', {}))
        else:
            self.votes = None
        if data.get('assignments'):
            self.assignments = AssignmentsContainer(
                data.get('assignments', {}))
        else:
            self.assignments = None
        if data.get('labels'):
            self.labels = LabelsContainer(data.get('labels', {}))
        else:
            self.labels = None
        self.form = SubmittedFormContainer(data.get('form', {}))
        self.files = []
        for data in data.get('files'):
            self.files.append(File(data))


class File(object):
    """
    Representation of files container as a Python object.

    :param data: Data dictionary in JSON format.
    :type data: str
    """
    def __init__(self, data):
        self.guid = data.get('guid', '')
        self.file_name = data.get('file_name', '')
        self.file_extension = data.get('file_extension', '')
        self.file_size = data.get('file_size', '')
        self.mime_type = data.get('mime_type', '')
        self.url = data.get('url', '')


class Votes(object):
    """
    Representation of Votes data as a Python object.

    :param data: Data dictionary in JSON format.
    :type data: str
    """
    def __init__(self, data):
        self.count = data.get('count', 0)
        self.score = data.get('score', 0)
        self.average = data.get('average', 0)


class SubmissionLabel(object):
    """
    Representation of Submission Label as a Python object.

    :param data: Data dictionary in JSON format.
    :type data: str
    """
    def __init__(self, data):
        self.label_text = data.get('label_text', '')
        self.label_color1 = data.get('label_color1', '')
        self.label_color2 = data.get('label_color2', '')


class SubmissionHistory(object):
    """
    Representation of Submission History as a Python object.

    :param data: Data dictionary in JSON format.
    :type data: str
    """
    def __init__(self, data):
        self.submission_id = data.get('submission_id', 0)
        self.history_type = data.get('history_type', '')
        self.history_date = data.get('history_date', '2001-01-01')
        self.is_private = data.get('is_private', False)
        self.is_visible_to_submitter = \
            data.get('is_visible_to_submitter', False)
        self.email_message = data.get('email_message', '')
        self.note = data.get('note', '')
        self.description = data.get('description', '')
        self.replace_data = data.get('replace_data', '')
        self.user = Submitter(data.get('user', {}))


class SubmittedFormContainer(object):
    """
    Representation of the Submitted Form container as a Python object.

    :param data: Data dictionary in JSON format.
    :type data: str
    """
    def __init__(self, data):
        self.type = data.get('type', '')
        self.url = data.get('url', '')
        self.count = data.get('count', len(data.get('items', [])))
        self.items = []
        for field_data in data.get('items', []):
            self.items.append(SubmittedFormField(field_data))


class SubmittedFormField(object):
    """
    Item container for a submitted form.

    :param data: Data dictionary in JSON format.
    :type data: str
    """
    def __init__(self, data):
        self.label = data.get('label', '')
        self.data = data.get('data', '')
        self.blind = data.get('blind', False)
        self.order = data.get('order', 0)


class Submitter(object):
    """
    Item object container for Submitters.

    :param data: Data dictionary in JSON format.
    :type data: str
    """
    def __init__(self, data):
        self.user_id = data.get('user_id', 0)
        self.first_name = data.get('first_name', '')
        self.last_name = data.get('last_name', '')
        self.email = data.get('email', '')


class LabelsContainer(object):
    """
    Representation of Labels Container as a Python object.

    :param data: Data dictionary in JSON format.
    :type data: str
    """
    def __init__(self, data):
        self.type = data.get('type', '')
        self.url = data.get('url', '')
        self.count = data.get('count', 0)
        self.items = []
        for label in data.get('items', []):
            self.items.append(SubmissionLabel(label))


class AssignmentsContainer(object):
    """
    Representation of Assignments Container as a Python object.

    :param data: Data dictionary in JSON format.
    :type data: str
    """
    def __init__(self, data):
        self.type = data.get('type', '')
        self.url = data.get('url', '')
        self.count = data.get('count', 0)
        self.items = []
        for assignment in data.get('items', []):
            self.items.append(Assignment(assignment))


class Assignment(object):
    """
    Representation of Assignment as a Python object.

    :param data: Data dictionary in JSON format.
    :type data: str
    """
    def __init__(self, data):
        self.user_id = data.get('user_id', 0)
        self.staff_name = data.get('staff_name', '')
        self.permission_level = data.get('permission_level', '')
        self.permission_value = data.get('permission_value', 0)


class FormFieldContainer(object):
    """
    Representation of the formfields dictionary as a Python object.

    :param data: Data dictionary in JSON format.
    :type data: str
    """
    def __init__(self, data):
        self.type = data.get('type', '')
        self.url = data.get('url', '')
        self.count = data.get('count', len(data.get('items', [])))
        self.items = []
        for field_data in data.get('items', []):
            self.items.append(FormFieldItem(field_data))


class FormFieldItem(object):
    """
    Representation of a formfield as a Python object.

    :param data: Data dictionary in JSON format.
    :type data: str
    """
    def __init__(self, data):
        self.label = data.get('label', '')
        self.description = data.get('description', '')
        self.field_type = data.get('field_type', '')
        self.blind = data.get('blind', False)
        self.order = data.get('order', 0)


class Category(object):
    """
    Item object container for Categories.

    :param data: Data dictionary in JSON format.
    :type data: str
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
