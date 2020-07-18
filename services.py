import requests

from constants import BASE_URL, league


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
            formatted_implicitMods = '\n'.join(self.listing['implicitMods']) + '\n' + '-'*60
            return formatted_implicitMods
        else:
            return None
    
    def format_explicitMods(self):
        """Format explicit mods, if they exist, into a string."""
        if 'explicitMods' in self.listing:
            formatted_explicitMods = '\n'.join(self.listing['explicitMods']) + '\n' + '-'*60
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
            self.rarity_type(), self.listing['name'], self.listing['typeLine'], '-'*60,
            self.format_properties(), self.format_requirements(), self.format_sockets(),
            f'Item Level: {self.listing["ilvl"]}', '-'*60, self.format_implicitMods(),
            self.format_explicitMods(), self.check_corruption(), self.check_identified(),
            self.format_price()
            ]
        filtered_item_info = [info for info in item_info if info is not None]
        formatted_item_info = '\n'.join(filtered_item_info)
        return formatted_item_info

def search_trade(search_info, trade_api, league=league):
    """
    Searches trade API for the first 5 related results.
    
    Args:
        search_info (dict | json): Form data for the search.
        trade_api (ApiRequests object): API Request object of the trade API.
        league (str): Current Path of Exile league.
    
    Returns:
        A dict of the response from the trade API.
    """
    post_response = trade_api.post('search/' + league, search_info)
    post_response = post_response.json()
    if 'error' in post_response:
        return post_response
    else:
        result = ','.join(post_response['result'][:5])
        get_response = poe_trade_api.get('fetch/' + result, params={'query': post_response['id']})
        get_response = get_response.json()
        all_listings = []
        for item in get_response['result']:
            listing = ListingObject.filter_dict(item) 
            all_listings.append(listing.item_info())
        return (f'\n{"="*60}\n'.join(all_listings))

poe_trade_api = ApiRequests(BASE_URL)
