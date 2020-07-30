# services.py
"""Access, filter and process API data.

Classes:
    ListingObjects

Functions:
    search_trade
    format_search_query
    image_from_url
    get_request
    post_request

"""

import requests
from requests.compat import urljoin
from io import BytesIO

from PIL import Image, ImageTk

from constants import TRADE_BASE_URL, league


class ListingObject:
    """Class for accessing and formatting the trade API response data.

    Args:
        search_result (dict): Individual listing from trade API response.

    """

    @classmethod
    def filter_dict(cls, d):
        """Class method to filter the input dict for relevant keys."""
        keys = (
            'name', 'typeLine', 'identified', 'ilvl', 'frameType', 'corrupted',
            'requirements', 'explicitMods', 'implicitMods', 'sockets', 'properties',
            'icon'
        )
        df = {key: val for key, val in d['item'].items() if key in keys}
        df['price'] = d['listing']['price']
        return cls(df)


    def __init__(self, search_result):
        """The constructor for the ListingObject class."""
        self.listing = search_result


    def format_price(self):
        """Formats the price into a string."""
        price_dict = self.listing["price"]
        price = f'{price_dict["type"]} {price_dict["amount"]} {price_dict["currency"]}'
        return price


    def rarity_type(self):
        """Returns the rarity of the item as a string."""
        rarity_dict = {0: 'Normal', 1: 'Magic', 2: 'Rare', 3: 'Unique'}
        return rarity_dict[self.listing['frameType']]


    def format_properties(self):
        """Formats the properties, if they exist, into a string."""
        if 'properties' in self.listing:
            properties = []
            for prop in self.listing['properties']:
                properties.append(f'{prop["name"]}: {prop["values"][0][0]}')
            formatted_properties = '\n'.join(properties) + '\n' + '-'*60
            return formatted_properties
        else:
            return None


    def format_requirements(self):
        """Formats the requirements, if they exist, into a string."""
        if 'requirements' in self.listing:
            requirements = ['Requirements']
            for req in self.listing['requirements']:
                requirements.append(f'{req["name"]}: {req["values"][0][0]}')
            formatted_requirements = '\n'.join(requirements) + '\n' + '-'*60
            return formatted_requirements
        else:
            return None


    def format_sockets(self):
        """Formats the sockets, if they exist, into a string."""
        if 'sockets' in self.listing:
            socketDict = {}
            for socket in self.listing['sockets']:
                if socket['group'] not in socketDict:
                    socketDict[socket['group']] = [socket['sColour']]
                else:
                    socketDict[socket['group']].append(socket['sColour'])
            for key, val in socketDict.items():
                socketDict[key] = '-'.join(val)
            formatted_sockets = ' '.join(socketDict.values()) + '\n' + '-'*60
            return formatted_sockets
        else:
            return None


    def format_implicitMods(self):
        """Format implicit mods, if they exist, into a string."""
        if 'implicitMods' in self.listing:
            formatted_implicitMods = '\n'.join(
                self.listing['implicitMods']) + '\n' + '-'*60
            return formatted_implicitMods
        else:
            return None


    def format_explicitMods(self):
        """Format explicit mods, if they exist, into a string."""
        if 'explicitMods' in self.listing:
            formatted_explicitMods = '\n'.join(
                self.listing['explicitMods']) + '\n' + '-'*60
            return formatted_explicitMods
        else:
            return None


    def check_corruption(self):
        """Check if the item is corrupted."""
        if 'corrupted' in self.listing:
            corruption = 'Corrupted'
            return corruption
        else:
            return None


    def check_identified(self):
        """Check if the item is identified."""
        if 'identified' == False:
            return 'Unidentified'
        else:
            return None


    def item_info(self):
        """Returns the relevant item information."""
        item_info = [
            self.rarity_type(),
            self.listing['name'],
            self.listing['typeLine'],
            '-'*60,
            self.format_properties(),
            self.format_requirements(), 
            self.format_sockets(),
            f'Item Level: {self.listing["ilvl"]}',
            '-' *60,
            self.format_implicitMods(),
            self.format_explicitMods(),
            self.check_corruption(),
            self.check_identified(),
            self.format_price()
        ]

        filtered_item_info = [info for info in item_info if info is not None]
        formatted_item_info = '\n'.join(filtered_item_info)
        return formatted_item_info


    def item_icon(self):
        """Returns the link to the item icon"""
        return self.listing['icon']


def search_trade_api(search_info, league=league):
    """Searches trade API for the first 10 related results.

    Converts API listings to ListingObjects.

    Args:
        search_info (dict | json): Form data for the search.
        trade_api (ApiRequests object): API Request object of the trade API.
        league (str): Current Path of Exile league.

    Returns:
        A list of ListingObjects.

    """
    post_response = post_request(TRADE_BASE_URL, 'search/' + league, search_info)
    # post_response = trade_api.post('search/' + league, search_info)
    post_response = post_response.json()
    if 'error' in post_response:
        return post_response
    else:
        result = ','.join(post_response['result'][:10])
        get_response = get_request(
            TRADE_BASE_URL, 'fetch/' + result, params={
                'query': post_response['id']
            }
        )
        # get_response = trade_api.get(
        #     'fetch/' + result, params={'query': post_response['id']})
        get_response = get_response.json()
        item_list = [
            ListingObject.filter_dict(item) for item in get_response['result']
        ]
        return item_list


def format_search_query(item_name, item_type):
    """Formats the search query into a dictionary for post requests.

    Args:
        item_name (str): Name of the item.
        item_type (str): Type of the item.

    Returns:
        A dictionary with search query parameters.

    """

    search_query_dict = {
        "query": {
            "status": {
                "option": "online"
            },
            "name": item_name,
            "type": item_type,
            "stats": [{
                "type": "and",
                "filters": []
            }]
        },
        "sort": {
            "price": "asc"
        }
    }
    return search_query_dict


def image_from_url(image_url):
    """Returns a Tkinter compatible photo image from a URL.
    
    Args:
        image_url (str): URL to the image.

    Returns:
        Tkinter compatible photo image.
    
    """
    r = requests.get(image_url)
    img = Image.open(BytesIO(r.content))
    photo = ImageTk.PhotoImage(img)
    return photo


def get_request(base_url, endpoint, params=None):
    """Sends a GET request to an endpoint with parameters and any cookies.

    Args:
        endpoint (str): The API endpoint.
        params (dict): Optional key-value pairs for query string parameters, defaults to None.

    Returns:
        request.Response object from get request.

    """

    get_url = urljoin(base_url, endpoint)
    response = requests.get(get_url, params=params, timeout=5)
    return response


def post_request(base_url, endpoint, payload):
    """Sends a POST request to an endpoint with a payload.

    Args:
        endpoint (str): The API endpoint.
        payload (json | dict): Payload to be sent with POST request.

    Returns:
        request.Response object from post request.

    """

    post_url = urljoin(base_url, endpoint)
    response = requests.post(post_url, json=payload)
    return response

