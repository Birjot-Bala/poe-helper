# poe_helper.py

import requests
from collections import namedtuple

league = 'Harvest'

search = {
    "query": {
        "status": {
            "option": "online"
        },
        "name": "The Pariah",
        "type": "Unset Ring",
        "stats": [{
            "type": "and",
            "filters": []
        }]
    },
    "sort": {
        "price": "asc"
    }
}


search2 = {
    "query": {
        "status": {
            "option": "online"
        },
        "name": "Bloodbond",
        "type": "Bone Armour",
        "stats": [{
            "type": "and",
            "filters": []
        }]
    },
    "sort": {
        "price": "asc"
    }
}


class ApiRequests:
    """
    Class for easy management of API URLs for GET and POST requests.

    Args:
        base_url (str): The base API URL without endpoints.
    """

    def __init__(self, base_url):
        """The constructor for the ApiRequests class."""
        self.base_url = base_url 
    
    # post request to API endpoint with json query
    def post(self, endpoint, payload):
        """
        Sends a POST request to an endpoint with a payload.
        
        Args:
            endpoint (str): The API endpoint.
            payload (json | dict): Payload to be sent with POST request. 
        """
        post_url  = self.base_url + endpoint
        post_response = requests.post(post_url, json=payload)
        return post_response
    
    # get request to API endpoint with optional parameters 
    def get(self, endpoint, params=None):
        """
        Sends a GET request to an endpoint with parameters and any cookies.

        Args:
            endpoint (str): The API endpoint.
            params (dict): Optional key-value pairs for query string parameters, defaults to None.
        """
        get_url = self.base_url + endpoint
        get_response = requests.get(get_url, params=params)
        return get_response


poe_trade_api = ApiRequests('https://www.pathofexile.com/api/trade')

def search_trade(search_info, trade_api=poe_trade_api, league=league):
    """
    Searches trade API for the first 5 related results.
    
    Args:
        search_info (dict | json): Form data for the search.
        trade_api (ApiRequests object): API Request object of the trade API.
        league (str): Current Path of Exile league.
    
    Returns:
        A dict of the response from the trade API.
    """
    post_response = trade_api.post('/search/' + league, search_info)
    post_response = post_response.json()
    result = ','.join(post_response['result'][:5])

    get_response = poe_trade_api.get('/fetch/' + result, params={'query': post_response['id']})
    get_response = get_response.json()
    
    return get_response


class ListingObject:
    """
    Class for accessing and formatting the trade API response data.

    Args:
        search_result (dict): Individual listing from trade API response.
    """

    @classmethod
    def filter_dict(cls, d):
        keys = (
            'name', 'typeLine', 'identified', 'ilvl', 'frameType', 'corrupted',
            'requirements', 'explicitMods', 'implicitMods', 'sockets', 'properties'
            )
        df = {key : val for key, val in d['item'].items() if key in keys}
        df['price'] = d['listing']['price']
        return cls(df)

    def __init__(self, search_result):
        """The constructor for the ListingObject class."""
        self.listing = search_result
        # self.name = search_result['item']['name']
        # self.type = search_result['item']['typeLine']
        # self.price = search_result['listing']['price']
        # self.identified = search_result['item']['identified']
        # self.ilvl = search_result['item']['ilvl']
        # self.frameType = search_result['item']['frameType']
        # self.corrupted = False
        # self.requirements = None
        # self.implicitMods = None

        # self.properties = None
        # self.sockets = None
        # self.identified = search_result['item']['identified']
        # if 'corrupted' in search_result['item']:
        #     self.corrupted = True
        # if self.identified == True:
        #     self.requirements = search_result['item']['requirements']
        #     self.explicitMods = search_result['item']['explicitMods']
        # if 'implicitMods' in search_result['item']:
        #     self.implicitMods = search_result['item']['implicitMods']
        # if 'sockets' in search_result['item']:
        #     self.sockets = search_result['item']['sockets']

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
            for prop in self.listing['properties']:
                print(f'{prop["name"]}: {prop["values"][0][0]}')
                print('-'*60)
        else:
            return None

    def format_requirements(self):
        """Formats the requirements, if they exist, into a string."""
        if 'requirements' in self.listing:
            print('Requirements:')
            for req in self.listing['requirements']:
                print(f'{req["name"]}: {req["values"][0][0]}')
                print('-'*60)
        else:
            return None
    
    def format_sockets(self):
        """Formats the sockets, if they exist, into a string."""
        if 'sockets' in self.listing:
            socketDict = {}
            socketGroup = 0
            for socket in self.listing['sockets']:
                if socket['group'] not in socketDict:
                    socketDict[socket['group']] = [socket['sColour']]
                else:
                    socketDict[socket['group']].append(socket['sColour'])
            for key, val in socketDict.items():
                socketDict[key] = '-'.join(val)
            print(' '.join(socketDict.values()))
            print('-'*60)
        else:
            return None

    def format_implicitMods(self):
        """Format implicit mods, if they exist, into a string."""
        if 'implicitMods' in self.listing:
            for mods in self.listing['implicitMods']:
                print(mods)
            print('-'*60)
        else:
            return None
    
    def format_explicitMods(self):
        """Format explicit mods, if they exist, into a string."""
        if 'explicitMods' in self.listing:
            for mods in self.listing['explicitMods']:
                print(mods)
            print('-'*60)

    def item_info(self):
        """Returns the relevant item information."""
        print(self.rarity_type())
        if self.listing['name'] is not '': 
            print(self.listing['name'])
        print(self.listing['typeLine'])
        print('-'*60)
        self.format_properties()
        self.format_requirements()
        self.format_sockets()
        print('Item Level:', self.listing['ilvl'])
        print('-'*60)
        self.format_implicitMods()
        self.format_explicitMods()
        print(self.format_price())           
    

response = search_trade(search)  

response2 = search_trade(search2)

for item in response['result']:
    listing = ListingObject.filter_dict(item)
    listing.item_info()