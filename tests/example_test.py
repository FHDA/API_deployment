import requests
import unittest
import urllib
from flask import Flask
from tests.app_test import BaseTest


class ExampleTest(BaseTest):
    def create_app(self):
        app = Flask(__name__)
        app.config["TESTING"] = True
        app.config["LIVESERVER_PORT"] = 5000
        app.config["LIVESERVER_TIMEOUT"] = 3
        return app

    def test_example_no_login_needed(self):
        response = requests.get(self.get_server_url())
        self.assertEqual(response.status_code, 200)

    def test_example_user_check(self):
        response = requests.get(
            self.get_server_url() + "/example_user_check/random_test_param"
        )
        self.assertEqual(response.status_code, 403)

    def test_example_admin_check(self):
        response = requests.get(
            self.get_server_url() + "/example_admin_check/random_test_param"
        )
        self.assertEqual(response.status_code, 403)

    def test_example_superadmin_check(self):
        response = requests.get(
            self.get_server_url() + "/example_superadmin_check/random_test_param"
        )
        self.assertEqual(response.status_code, 403)


if __name__ == "__main__":
    unittest.main()
