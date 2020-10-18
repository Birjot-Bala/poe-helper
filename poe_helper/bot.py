from discord.ext import commands

from poe_helper.parsers import item_parser
from poe_helper.services import create_search_query, search_trade_api


bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='price', help='Looks up item on Path of Exile trade.')
async def price(ctx, *, arg):
    try:
        parsed_item = item_parser(arg)
        trade_response = search_trade_api(
            create_search_query(parsed_item)
        )
        message = f'{parsed_item["name"]}\n{parsed_item["type"]}\n'
        for listing in trade_response:
            message += '\n' + listing.format_price()
        formatted_message = "```" + message + "```"
        await ctx.send(formatted_message)
    except:
        await ctx.send("Something went wrong. Make sure the item text " + 
            "has been pasted correctly.")