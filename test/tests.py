import unittest

from fiesta import FiestaAPI, FiestaAPISandbox, FiestaGroup, FiestaUser
from settings_test import FIESTA_CLIENT_ID, FIESTA_CLIENT_SECRET


class FiestaBaseTestCase(unittest.TestCase):
    api = None

    def setUp(self):
        self.api = FiestaAPISandbox(client_id=FIESTA_CLIENT_ID, client_secret=FIESTA_CLIENT_SECRET)
        self.api.reset()


class FiestaListManagementTestCase(FiestaBaseTestCase):

    def test_should_get_hello(self):
        result = self.api.hello()

        self.assertTrue(result is not None, msg=u"Result did not return anothing")
        self.assertTrue('hello' in result, msg=u"Response does not have a hello key in the dictionary")
        self.assertEqual(result['hello'], 'world', msg=u"Hello world was not returned")

    def test_should_create_group(self):
        group = FiestaGroup.create(self.api, description=u"A group made by the fiesta test suite")

        self.assertTrue(group.id is not None, msg=u"Group ID doesn't exist")
        self.assertTrue(len(group.id) > 1, msg=u"Group ID doesn't exist")

    def test_should_add_member_to_group(self):
        group_name = 'test-suite-group'
        new_group = FiestaGroup.create(self.api, default_name=group_name, description=u"A group made by the fiesta test suite")

        group = FiestaGroup(self.api, id=new_group.id)   # could just re-use the group above, but this also tests the group init process
        user = group.add_member('test@example.com', member_display_name='Test User')

        self.assertTrue(user is not None, msg=u"User does not exist")
        self.assertTrue(len(user.id) > 1, msg=u"User ID was not stored")
#        self.assertTrue()  # test that user_group_name matches default_group_name
