import requests
import unittest
import urllib
import json
import time
import multiprocessing
import pytest
from flask import Flask
from flask_testing import LiveServerTestCase

multiprocessing.set_start_method("fork")


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

    @pytest.mark.skip(reason="Only enable at local or on server, will add config later")
    def test_example_hashtag(self):
        example_hashtag = {"tag": "pytest_check", "display": 1}
        requests.delete(self.get_server_url() + "/hashtag", data=example_hashtag)
        try:
            response = requests.post(
                self.get_server_url() + "/hashtag", data=example_hashtag
            )
            self.assertEqual(response.status_code, 200)

            time.sleep(0.5)
            response = requests.get(
                self.get_server_url() + "/hashtag", data={"tag": "pytest_check"}
            )
            self.assertEqual(response.status_code, 200)
            response_content = json.loads(response.content)
            self.assertEqual(response_content[0]["name"], example_hashtag["tag"])
            self.assertEqual(
                response_content[0]["is_display"], example_hashtag["display"]
            )

            time.sleep(0.5)
            response = requests.get(
                self.get_server_url() + "/hashtag",
                data={"tag": "this_is_a_tag_that_does_not_exist!"},
            )
            self.assertEqual(response.status_code, 404)

            time.sleep(0.5)
            response = requests.put(
                self.get_server_url() + "/hashtag",
                data={"tag": "pytest_check", "display": 0},
            )
            self.assertEqual(response.status_code, 200)

            time.sleep(0.5)
            response = requests.get(
                self.get_server_url() + "/hashtag", data={"tag": "pytest_check"}
            )
            self.assertEqual(response.status_code, 200)
            response_content = json.loads(response.content)
            self.assertEqual(response_content[0]["name"], example_hashtag["tag"])
            self.assertEqual(response_content[0]["is_display"], 0)

            time.sleep(0.5)
            response = requests.delete(
                self.get_server_url() + "/hashtag", data={"tag": "pytest_check"}
            )
            self.assertEqual(response.status_code, 200)

            response = requests.get(
                self.get_server_url() + "/hashtag", data={"tag": "pytest_check"}
            )
            self.assertEqual(response.status_code, 404)
        except AssertionError as e:
            requests.delete(self.get_server_url() + "/hashtag", data=example_hashtag)
            pytest.fail(str(e))


if __name__ == "__main__":
    unittest.main()
