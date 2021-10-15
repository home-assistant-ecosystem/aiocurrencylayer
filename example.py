"""Sample code for interacting with the currencylayer API."""
import asyncio

from aiocurrencylayer import CurrencyLayer

API_KEY = "YOUR_API_KEY"
QUOTE = "CHF"
SOURCE = "USD"


async def main():
    """The main part of the example script."""
    currency = CurrencyLayer(API_KEY, source=SOURCE)

    # Get the data
    await currency.get_data()

    # Validate the API key
    if currency.validate_api_key is False:
        print(currency.data["error"]["info"].split(".")[0])

    print("Supported currencies:", len(currency.supported_currencies))

    # Get all quotes (identical to currency.quotes), use quote=CURRENCY
    # to initialize the object to only get one currency
    print(currency.quote)

    # Get a single quote
    print(QUOTE, currency.quotes[QUOTE])


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
