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
