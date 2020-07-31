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


def test_get_request(mock_requests):
    result = se.get_request("https://fake.url/", "fake endpoint")
    assert isinstance(result, MockResponse) == True


def test_post_request(mock_requests):
    result = se.post_request("https://fake.url/", "fake endpoint", "fake query")
    assert isinstance(result, MockResponse) == True


def test_search_trade_api(mock_requests):
    with open('tests/data/pariah_ring_search.json') as json_file:
        test_search = json.load(json_file)
    test_search_output = se.search_trade_api(
        test_search, 'fake league')
    assert isinstance(test_search_output, list) == True
    for i in test_search_output:
        assert isinstance(i, se.ListingObject) == True

def test_create_search_query():
    test_search_query = se.create_search_query({
        'Requirements': {
            'Level': '17', 
            'Dex': '62'
        },
        'type': 'Basket Rapier',
        'name': 'Death Scalpel',
        'corrupted': True,
        'Rarity': 'Rare',
        'properties': {
            'Physical Damage': '13-30 (augmented)', 
            'Elemental Damage': '1-4 (augmented), 2-25 (augmented)',
            'Critical Strike Chance': '5.50%', 
            'Attacks per Second': '1.55', 
            'Weapon Range': '14'
        },
        'Sockets': 'R-G-R',
        'Item Level': '17',
        'implicitMods': [
            '+25% to Global Critical Strike Multiplier (implicit)'
        ],
        'Note': '~price 1 jewellers',
        'explicitMods': [
            '+8 to Dexterity',
            '21% increased Physical Damage',
            'Adds 1 to 4 Fire Damage',
            'Adds 2 to 25 Lightning Damage', 
            '+7% to Fire Resistance', 
            '+8% to Chaos Resistance', 
            '+32 to Accuracy Rating'
        ]
    })

    assert test_search_query["query"]["type"] == "Basket Rapier"
