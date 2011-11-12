import json
import base64
import urllib2


# Left to be implemented
# http://docs.fiesta.cc/list-management-api.html#adding-members
# http://docs.fiesta.cc/list-management-api.html#sending-messages
# http://docs.fiesta.cc/list-management-api.html#messages
# http://docs.fiesta.cc/list-management-api.html#removing-a-list-member
# http://docs.fiesta.cc/list-management-api.html#getting-group-user-information
# http://docs.fiesta.cc/list-management-api.html#getting-group-user-information



class FiestaAPI(object):
    """
    A Python wrapper to the Fiesta.cc API: http://docs.fiesta.cc/
    """
    base_uri = "https://api.fiesta.cc/%s"

    trusted_client = True # Will help later when abstracting this code to handle

    client_id = None
    client_secret = None
    # see http://docs.fiesta.cc/list-management-api.html#creating-a-group
    domain = None
    # Fallback email address to use as owner of lists
    default_address = None

    # Strore recent request and response information
    _last_request = None
    _last_response = None
    _last_response_str = None

    def __init__(self, client_id=None, client_secret=None, domain=None, default_address=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.domain = domain
        self.default_address = default_address

    @property
    def group(self):
        """
        Easy access to group methods. Creates a new group each time it is accessed.

        Allows you to easily do things like:
            f = FiestaAPI(id, secret)
            group = f.group.create(description='my group')
        """
        return self.FiestaGroup(self)

    def request(self, request_path, data=None, do_authentication=True, is_json=True):
        """
        Core "worker" for making requests and parsing JSON responses. Data should be a dictionary structured to match
        the fiesta docs.
        """
        uri = self.base_uri % request_path
        request = urllib2.Request(uri)

        # Build up the request
        if is_json:
            request.add_header("Content-Type", "application/json")
        if do_authentication:
            if self.client_id is None or self.client_secret is None:
                raise Exception(u"You need to supply a client_id and client_secret to perform an authetnicated requrest")
            basic_auth = base64.b64encode("%s:%s" % (self.client_id, self.client_secret))
            request.add_header("Authorization", "Basic %s" % basic_auth)
        if data is not None:
            request.add_data(json.dumps(data))

        # TODO: I'm sure all kinds of error checking needs to go here
        response_raw = urllib2.urlopen(request)
        response_str = response_raw.read()
        response = json.loads(response_str)
        self._last_request = request
        self._last_response = response_raw
        self._last_response_str = response_str
        return response

    def hello(self):
        """http://docs.fiesta.cc/index.html#getting-started"""
        path = 'hello'
        response = self.request(path, do_authentication=False)
        return response


    class FiestaGroup(object):
        api = None

        # Fiesta supports each group member having a different address for the group, but the current implementation
        # assumes all members of the group will use the same group_name.
        name = None
        description = None
        domain = None
        group_id = None
        group_uri = None
        members_uri = None

        def __init__(self, api):
            if api is None:
                api = FiestaAPI()

            self.api = api

        def __unicode__(self):
            return "%s -- %s" % (self.name, self.description)

        def create(self, group_name=None, address=None, display_name=None, description=None, members=None):
            """
            http://docs.fiesta.cc/list-management-api.html#creating-a-group

            200 character max on the description.
            If the client is not trusted, address is required
            """
            path = 'group'

            data = {}
            if not self.api.trusted_client:
                # TODO: Not implemented yet. Need to suppply token of you're going this route. See docs.
                data['creator'] = {}
                if address is None:
                    address = self.api.default_address
                if address:
                    data['creator']['address'] = address
                else:
                    # TODO: Throw an error
                    pass
                if group_name:
                    data['creator']['group_name'] = group_name
                if display_name:
                    data['creator']['display_name'] = display_name

            # If trusted, these are the only arguments that are available
            if description:
                data['description'] = description
            if self.api.domain:
                data['domain'] = self.api.domain

            response = self.api.request(path, data=data)
            self._absorb_data(response['data'])
            return self

        def _absorb_data(self, data):
            """
            Takes a the data from a fiesta request and absorbs it into object-level properties
            """
            self.description = data['description']
            self.domain = data['domain']
            self.group_id = data['group_id']
            self.group_uri = data['group_uri']
            self.members_uri = data['members']










#def create_group_trusted():
#    create_group_uri = "https://api.fiesta.cc/group"
#
#    api_inputs = {}
#
#    response = _create_and_send_request(create_group_uri, api_inputs)
#    json_response = json.loads(response.read())
#
#    group_id = json_response['data']['group_id']
#
#
#def add_member_trusted(group_id, member_email, group_name):
#    add_member_uri = "https://api.fiesta.cc/membership/%s"
#
#    api_inputs = {'group_name': group_name,
#                  'address': member_email}
#
#    _create_and_send_request(add_member_uri % group_id, api_inputs)
