import json
import multiprocessing
import pytest
import requests
import time
import unittest
import urllib
from flask import Flask
from tests.app_test import BaseTest


class MiscellaneousTest(BaseTest):
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
