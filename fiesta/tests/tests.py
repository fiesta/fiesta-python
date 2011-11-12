import unittest

from fiesta import FiestaAPI, FiestaGroup, FiestaUser
from fiesta.tests.settings_test import FIESTA_CLIENT_ID, FIESTA_CLIENT_SECRET

class FiestaBaseTestCase(unittest.TestCase):
    api = None

    def setUp(self):
        self.api = FiestaAPI(client_id=FIESTA_CLIENT_ID, client_secret=FIESTA_CLIENT_SECRET)


class TestApiBasics(FiestaBaseTestCase):


    def test_should_get_hello(self):
        result = self.api.hello()

        self.assertEqual(result['hello'], 'world', msg=u"Hello world was not returned")

    def test_should_create_group(self):
        group = FiestaGroup.create(self.api, description=u"A group made by the fiesta test suite")

        self.assertTrue(group.id is not None, msg=u"Group ID doesn't exist")
        self.assertTrue(len(group.id) > 1, msg=u"Group ID doesn't exist")