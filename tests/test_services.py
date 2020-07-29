# test_services.py

import requests
import json
from pathlib import Path

import pytest

import poe_helper.services as se

data_folder = Path("tests/data/")

# mock response class
class MockResponse():

    def __init__(self, json_path):
        self.path = json_path

    @staticmethod
    def status_code():
        return 200

    @staticmethod
    def ok():
        return True

    def json(self):
        with open(self.path) as json_file:
            test_response = json.load(json_file)
        return test_response

    def __repr__(self):
        return f'<Response [{self.status_code()}]>'


# mock requests
@pytest.fixture
def mock_requests(monkeypatch):

    def mock_get(*args, **kwargs):
        return MockResponse(data_folder / "pariah_ring_get_response.json")

    def mock_post(*args, **kwargs):
        return MockResponse(data_folder / "pariah_ring_post_response.json")

    monkeypatch.setattr(requests, "get", mock_get)
    monkeypatch.setattr(requests, "post", mock_post)


# mock ApiRequests class
@pytest.fixture
def test_ApiRequests_object(mock_requests):
    return se.ApiRequests('https://fakeurl.com')


def test_ApiRequests_get(test_ApiRequests_object):
    result = test_ApiRequests_object.get("fake endpoint")
    assert isinstance(result, MockResponse) == True


def test_ApiRequests_post(test_ApiRequests_object):
    result = test_ApiRequests_object.post("fake endpoint", "fake query")
    assert isinstance(result, MockResponse) == True


def test_search_trade_api(test_ApiRequests_object):
    with open('tests/data/pariah_ring_search.json') as json_file:
        test_search = json.load(json_file)
    test_search_output = se.search_trade_api(
        test_search, test_ApiRequests_object, 'fake league')
    assert isinstance(test_search_output, list) == True
    for i in test_search_output:
        assert isinstance(i, se.ListingObject) == True

def test_format_search_query():
    test_search_query = se.format_search_query("test_name", "test_type")
    assert test_search_query["query"]["name"] == "test_name"
    assert test_search_query["query"]["type"] == "test_type"
