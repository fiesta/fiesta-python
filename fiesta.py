import base64, json, urllib2

api_client_id = "Send an email to Fiesta.cc to get an API ID/Secret"
api_client_secret = ""
basic_auth = base64.b64encode("%s:%s" % (api_client_id, api_client_secret))

def _create_and_send_request(uri, api_inputs):
    request = urllib2.Request(uri)
    request.add_header("Authorization", "Basic %s" % (basic_auth))
    request.add_header("Content-Type", "application/json")
    request.add_data(json.dumps(api_inputs))

    return urllib2.urlopen(request)


def create_group_trusted():
    create_group_uri = "https://api.fiesta.cc/group"

    api_inputs = {}

    response = _create_and_send_request(create_group_uri, api_inputs)
    json_response = json.loads(response.read())

    group_id = json_response['data']['group_id']


def add_member_trusted(group_id, member_email, group_name):
    add_member_uri = "https://api.fiesta.cc/membership/%s"

    api_inputs = {'group_name': group_name,
                  'address': member_email}

    _create_and_send_request(add_member_uri % group_id, api_inputs)
