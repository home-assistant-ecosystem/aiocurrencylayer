"""Sample code for the wrapper to interact with the CurrencyLayer API."""
import asyncio

import aiohttp

from aiocurrencylayer import CurrencyLayer

API_KEY = 'YOUR_CURRENCYLAYER_API_KEY'
QUOTE = 'CHF'
SOURCE = 'USD'


async def main():
    """The main part of the example script."""
    async with aiohttp.ClientSession() as session:
        currency = CurrencyLayer(loop, session, API_KEY, source=SOURCE)

        # Get the data
        await currency.get_data()

        # Validate the API key
        if await currency.validate_api_key() is False:
            print(currency.data['error']['info'].split('.')[0])
            return

        # Check if it's a free plan
        if await currency.check_free_plan() is True:
            print(
                "An API key for free plan is used, only USD as source allowed")
            return

        print(currency.quotes)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
