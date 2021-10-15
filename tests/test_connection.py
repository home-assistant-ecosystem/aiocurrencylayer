"""Test the interaction with the currencylayer API."""
import pytest
from pytest_httpx import HTTPXMock

from aiocurrencylayer import CurrencyLayer
import httpx


API_KEY = "YOUR_API_KEY"
QUOTE = "ZMW"
SOURCE = "USD"

RESPONSE_VALID = {
    "success": True,
    "terms": "https://currencylayer.com/terms",
    "privacy": "https://currencylayer.com/privacy",
    "timestamp": 1634285343,
    "source": "USD",
    "quotes": {
        "USDAED": 3.67298,
        "USDAFN": 90.115577,
        "USDALL": 105.00304,
        "USDZMW": 16.924404,
        "USDZWL": 321.999592,
    },
}


@pytest.mark.asyncio
async def test_timeout(httpx_mock: HTTPXMock):
    """Test if the connection is hitting the timeout."""

    def raise_timeout(request, extensions: dict):
        """Set the timeout for the requests."""
        raise httpx.ReadTimeout(
            f"Unable to read within {extensions['timeout']}", request=request
        )

    httpx_mock.add_callback(raise_timeout)

    with pytest.raises(httpx.ReadTimeout):
        client = CurrencyLayer(API_KEY)
        await client.get_data()


@pytest.mark.asyncio
async def test_quote(httpx_mock: HTTPXMock):
    """Test a quote."""
    httpx_mock.add_response(json=RESPONSE_VALID)

    client = CurrencyLayer(API_KEY)
    await client.get_data()

    assert client.quotes[QUOTE] == 16.9244


@pytest.mark.asyncio
async def test_supported_currencies(httpx_mock: HTTPXMock):
    """Test the supported currencies."""
    httpx_mock.add_response(json=RESPONSE_VALID)

    client = CurrencyLayer(API_KEY)
    await client.get_data()

    assert len(client.supported_currencies) == 5
