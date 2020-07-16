# poe_helper.py

import requests

league = 'Harvest'

# Handling API URLs
class api_requests:

    def __init__(self, base_url):
        self.base_url = base_url 
    
    # post request to API endpoint with json query
    def post(self, endpoint, query):
        post_url  = self.base_url + endpoint
        post_response = requests.post(post_url, json=query)
        return post_response
    
    # get request to API endpoint with optional parameters 
    def get(self, endpoint, params=None, cookies=None):
        get_url = self.base_url + endpoint
        get_response = requests.get(get_url, params=params, cookies=cookies)
        return get_response




poe_trade_api = api_requests('https://www.pathofexile.com/api/trade')

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

def search_trade(search_payload, trade_api=poe_trade_api, league=league):
    # searches trade api for the first 10 related results
    post_response = trade_api.post('/search/' + league, search_payload)
    post_response = post_response.json()
    result = ','.join(post_response['result'][:10])

    get_response = poe_trade_api.get('/fetch/' + result, params={'query': post_response['id']})
    get_response = get_response.json()
    
    return get_response


response = search_trade(search)

for i in response['result']:
    print(i['item']['implicitMods'])

        