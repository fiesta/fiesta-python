import base64
import json
import urllib2


class FiestaAPI(object):
    """
    A Python wrapper to the Fiesta.cc API: http://docs.fiesta.cc/
    """
    base_uri = "https://api.fiesta.cc/%s"

    client_id = None
    client_secret = None

    def __init__(self, client_id=None, client_secret=None):
        self.client_id = client_id
        self.client_secret = client_secret

    def request(self, request_path, data=None, authenticate=True):
        uri = self.base_uri % request_path
        request = urllib2.Request(uri)

        request.add_header("Content-Type", "application/json")

        if authenticate:
            basic_auth = base64.b64encode("%s:%s" % (self.client_id, self.client_secret))
            request.add_header("Authorization", "Basic %s" % basic_auth)

        if data is not None:
            request.add_data(json.dumps(data))

        response = urllib2.urlopen(request).read()
        return response

    def hello(self):
        """http://docs.fiesta.cc/index.html#getting-started"""
        path = 'hello'
        response = self.request(path, authenticate=False)
        return response




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
