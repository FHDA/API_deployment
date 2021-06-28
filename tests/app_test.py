import requests
import unittest
import urllib
from flask import Flask
from flask_testing import LiveServerTestCase


class BaseTest(LiveServerTestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config["TESTING"] = True
        app.config["LIVESERVER_PORT"] = 5000
        app.config["LIVESERVER_TIMEOUT"] = 3
        return app

    def test_server_is_up_and_running(self):
        response = urllib.request.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)

    def test_example_access_token_check(self):
        response = requests.get(self.get_server_url() + "/example_access_token_check")
        self.assertEqual(response.status_code, 403)

    def test_example_id_token_check(self):
        response = requests.get(self.get_server_url() + "/example_id_token_check")
        self.assertEqual(response.status_code, 403)


if __name__ == "__main__":
    unittest.main()
