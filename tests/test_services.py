# test_services.py

import requests

import pytest

import services

# mock response class
class MockResponse:

    @staticmethod
    def json():
        return {"mock_key": "mock_response"}

    @staticmethod
    def status_code():
        return 200

    @staticmethod
    def ok():
        return True

    def __repr__(self):
        return f'<Response [{self.status_code()}]>'

        

# mock requests
@pytest.fixture
def mock_requests(monkeypatch):

    def mock_get(*args, **kwargs):
        return MockResponse()
    
    def mock_post(*args, **kwargs):
        return MockResponse()
    
    monkeypatch.setattr(requests, "get", mock_get)
    monkeypatch.setattr(requests, "post", mock_post)

# mock ApiRequests class
@pytest.fixture
def test_ApiRequests_object(mock_requests):
    return services.ApiRequests('https://fakeurl.com')

def test_ApiRequests_get(test_ApiRequests_object):
    result = test_ApiRequests_object.get("fake endpoint")
    assert isinstance(result, MockResponse) == True

def test_ApiRequests_post(test_ApiRequests_object):
    result = test_ApiRequests_object.post("fake endpoint", "fake query")
    assert isinstance(result, MockResponse) == True