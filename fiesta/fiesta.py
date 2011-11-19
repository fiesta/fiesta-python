# Copyright 2011 Fiesta Technology, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######
# Authors:
#  Jeremy Blanchard (auzigog@gmail.com) - Nov 2011 - Initial list management wrapper

import json
import base64
import urllib2


# Left to be implemented
# http://docs.fiesta.cc/list-management-api.html#removing-a-list-member
# http://docs.fiesta.cc/list-management-api.html#getting-group-user-information
# http://docs.fiesta.cc/list-management-api.html#getting-group-user-information



class FiestaAPI(object):
    """
    A Python wrapper for the Fiesta API: http://docs.fiesta.cc/
    """
    api_uri = 'https://api.fiesta.cc/%s'

    client_id = None
    client_secret = None
    domain = None               # For custom domain support

    # Store recent request and response information
    _last_request = None
    _last_response = None
    _last_response_str = None
    _last_status_code = None
    _last_status_message = None

    def __init__(self, client_id=None, client_secret=None, domain=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.domain = domain

    def request(self, request_path, data=None, do_authentication=True, is_json=True):
        """
        Core "worker" for making requests and parsing JSON responses.

        If `is_json` is ``True``, `data` should be a dictionary which
        will be JSON-encoded.
        """
        uri = self.api_uri % request_path
        request = urllib2.Request(uri)

        # Build up the request
        if is_json:
            request.add_header("Content-Type", "application/json")
            if data is not None:
                request.add_data(json.dumps(data))
        elif data is not None:
            request.add_data(data)

        if do_authentication:
            if self.client_id is None or self.client_secret is None:
                raise Exception(u"You need to supply a client_id and client_secret to perform an authenticated request")
            basic_auth = base64.b64encode("%s:%s" % (self.client_id, self.client_secret))
            request.add_header("Authorization", "Basic %s" % basic_auth)

        try:
            response = self._make_request(request)
        except Exception as inst:
            raise # automatically re-raises the exception

        if 'status' in response:
            # Grab the status info if it exists
            self._last_status_code = response['status']['code']
            if 'message' in response['status']:
                self._last_status_message = response['status']['message']

            if 'data' in response:
                return response['data']

        return response

    def _make_request(self, request):
        """
        Does the magic of actually sending the request and parsing the response
        """
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
    
    def create_group(self, **kwargs):
        """Helper function for creating groups"""
        return FiestaGroup.create(self, **kwargs)



class FiestaGroup(object):
    api = None

    # Fiesta supports each group member having a different address
    # pointing to the same group. The FiestaGroup name property is the
    # default that the group will use if you don't choose to override
    # this on a per-member basis.
    name = None
    description = None
    id = None

    def __init__(self, api, id=None, name=None, description=None):
        if api is None:
            api = FiestaAPI()
        self.api = api

        self.id = id
        self.name = name
        self.description = description

    def __unicode__(self):
        return "%s: %s" % (self.name, self.description)

    @staticmethod
    def create(api, name=None, description=None, members=None):
        """
        http://docs.fiesta.cc/list-management-api.html#creating-a-group

        200 character max on the description.
        """
        path = 'group'

        data = {}
        if description:
            data['description'] = description
        if api.domain:
            data['domain'] = api.domain

        response_data = api.request(path, data=data)

        id = response_data['group_id']
        group = FiestaGroup(api, id)
        group.name = name

        # TODO: Allow members to be passed in and auto created using this function

        return group

    @staticmethod
    def by_id(api, id):
        pass

    def guess_name_from_first_user(self, user_id=None):
        """
        Since group names *may* be specified on a per-member basis, knowing the group ID doesn't give us the `name` or
        `display_name`. This method loads the `name` and `display_name` from the first user.

        If you specify a User ID to load it from, this method only requires one API request.
        If you do not specify a User ID, this method requires two API requests.
        """
        # TODO: Finish implementing this function
        if user_id is None:
            # TODO: get membership list
            pass

        # Load the group name

    def add_member(self, address, group_name=None, member_display_name=None, welcome_message=None):
        """
        Add a member to a group. http://docs.fiesta.cc/list-management-api.html#adding-members

        `group_name` Since each member can access a group using their own name, you can override the `group_name` in
        this method. By default, the group will have the name specified on the class level `group_name` property.

        `display_name` is the full name of the user that they will see throughout the UI if this is a new account.
        `welcome_message` should be a dictionary specified according to the docs. If you set it to False, no message
        will be sent. See http://docs.fiesta.cc/list-management-api.html#message for formatting details.
        """

        # TODO: Move this requirement to a decorator
        if self.id is None:
            raise Exception(u"Must specify a group ID when adding a member. Try calling FiestaGroup.by_id().")

        path = 'membership/%s' % self.id
        data = { 'address': address }

        group_name = group_name or self.name
        if group_name:
            data['group_name'] = group_name

        if member_display_name:
            data['display_name'] = member_display_name

        if welcome_message:
            data['welcome_message'] = welcome_message
        elif welcome_message is False:
            data['welcome_message'] = 'false'  # Do not send a welcome message

        response_data = self.api.request(path, data)
        user_id = response_data['user_id']
        user = FiestaUser(user_id, address=address, groups=[self])
        return user

    def send_message(self, subject=None, text=None, markdown=None, message_dict=None):
        """
        Helper function to send a message to a group
        """
        message = FiestaMessage(self.api, self, subject, text, markdown, message_dict)
        return message.send()

class FiestaUser(object):
    """
    Represents a fiesta user.
    """
    id = None
    address = None      # Can't actually be retreived from the API, but can be stored here for your conveinence
    groups = None       # A python list of FiestaGroup objects

    def __init__(self, id, address=None, groups=None):
        self.id = id
        self.address = address
        self.groups = groups

    @staticmethod
    def by_id(api):
        pass

    def load_groups(self):
        # TODO: Implement the ability to load all of this members groups
        pass


class FiestaMessage(object):
    """
    A fiesta message.
    """
    api = None

    group = None

    subject = None
    text = None
    markdown = None  # If you only specify markdown, it will use it as the plaintext version as well

    id = None
    thread_id = None
    sent_message = None  # Holds a FiestaMessage returned by the most recent sent_message that fiesta returned.

    def __init__(self, api, group=None, subject=None, text=None, markdown=None, message_dict=None):
        """
        Create a new message object.

        If `message` is provided, then `subject`/`text`/`markdown` will be ignored.
        """
        self.api = api

        self.group = group

        if message_dict is not None:
            self._load_message(message_dict)
        else:
            self.subject = subject
            self.text = text
            self.markdown = markdown

    def _load_message(self, message_dict):
        if 'subject' in message_dict:
            self.subject = message_dict['subject']
        if 'text' in message_dict:
            self.text = message_dict['text']
        if 'markdown' in message_dict:
            self.markdown = message_dict['markdown']

    def send(self, group_id=None, message_dict=None):
        """
        Send this current message to a group.

        `message_dict` can be a dictionary formatted according to http://docs.fiesta.cc/list-management-api.html#messages
        If message is provided, this method will ignore object-level variables.
        """
        if self.group is not None and self.group.id is not None:
            group_id = self.group.id

        path = 'message/%s' % group_id

        if message_dict is not None:
            request_data = {
                'message': message_dict,
            }
        else:
            subject = self.subject
            text = self.text
            markdown = self.markdown

            request_data = {
                'message': {},
            }
            if subject:
                request_data['message']['subject'] = subject
            if text:
                request_data['message']['text'] = text
            if markdown:
                request_data['message']['markdown'] = markdown

        response_data = self.api.request(path, request_data)

        self.id = response_data['message_id']
        self.thread_id = response_data['thread_id']
        self.sent_message = FiestaMessage(self.api, response_data['message'])

        # Can't think of any logical return here


class FiestaAPISandbox(FiestaAPI):
    """
    Sandbox version of the API that can be used for testing purposes without sending real emails or modifying real objects
    http://docs.fiesta.cc/sandbox.html
    """
    api_uri = 'https://sandbox.fiesta.cc/%s'

    def mailbox(self):
        """
        Get a dictionary containing email addresses of people who have received messages from the sandbox
        http://docs.fiesta.cc/sandbox.html#get--mailbox

        Structured like this:
            {
              mike@corp.fiesta.cc: [
                {
                  text: "Hello world.",
                  subject: "Saying hello"
                },
                ...
              ],
              ...
            }
        """
        path = 'mailbox'
        response_data = self.request(path)
        return response_data

    def reset(self):
        """
        Reset the state of the sandbox.
        http://docs.fiesta.cc/sandbox.html#post--reset
        """
        path = 'reset'
        response_data = self.request(path)
        success = response_data['reset']   # True of False
        return success
