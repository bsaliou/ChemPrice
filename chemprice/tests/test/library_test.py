import unittest
from unittest.mock import MagicMock
import requests
import unittest
import os
import sys


# Add path
sys.path.insert(0, os.path.abspath('..'))
from chemprice import chemprice as cp



class TestPriceCollector(unittest.TestCase):




    def setUp(self):
        self.price_collector = cp.PriceCollector()




    def test_setMolportUsername(self):
        self.price_collector.setMolportUsername("test_username")
        self.assertEqual(self.price_collector.login['molport_username'], "test_username")




    def test_setMolportPassword(self):
        self.price_collector.setMolportPassword("test_password")
        self.assertEqual(self.price_collector.login['molport_password'], "test_password")




    def test_setMolportApiKey(self):
        self.price_collector.setMolportApiKey("880d8343-8ui2-418c-9g7a-68b4e2e78c8b")
        self.assertEqual(self.price_collector.login['molport_api_key'], "880d8343-8ui2-418c-9g7a-68b4e2e78c8b")




    def test_setChemSpaceApiKey(self):
        self.price_collector.setChemSpaceApiKey("test_api_key")
        self.assertEqual(self.price_collector.login['chemspace_api_key'], "test_api_key")




    def test_setMCuleApiKey(self):
        self.price_collector.setMCuleApiKey("test_api_key")
        self.assertEqual(self.price_collector.login['mcule_api_key'], "test_api_key")




    def test_add_to_the_dictionnary(self):
        instance = MagicMock()
        self.price_collector.add_to_the_dictionnary(instance)
        self.assertIn(instance, cp.PriceCollector.instances)




    def test_check_with_invalid_credentials(self):
        # Mock the requests.post function to simulate a failed response
        mock_post = MagicMock()
        mock_post.return_value.json.return_value = {"Result": {"Status": 0}}
        requests.post = mock_post

        result = self.price_collector.check()

        self.assertEqual(result, 0)
        self.assertFalse(self.price_collector.molport_id_valid)
        self.assertFalse(self.price_collector.molport_api_key_valid)




if __name__ == '__main__':
    unittest.main()
