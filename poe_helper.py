# poe_helper.py

from services import poe_trade_api, search_trade_api, format_search_query


search_pariah = format_search_query("The Pariah", "Unset Ring")
response_pariah = search_trade_api(search_pariah, poe_trade_api)

print('\n\n'.join([item.item_info() for item in response_pariah]))
