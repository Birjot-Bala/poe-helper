# poe_helper.py

from services import poe_trade_api, search_trade

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
         
    
response1 = search_trade(search, poe_trade_api)
print(response1)

#response2 = search_trade(search2, poe_trade_api)