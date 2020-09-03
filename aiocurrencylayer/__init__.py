"""Wrapper for interacting with the currencylayer API."""
import asyncio
import logging

import aiohttp
import async_timeout

from . import exceptions

_LOGGER = logging.getLogger(__name__)
_RESOURCE = "http://apilayer.net/api/live"


class CurrencyLayer(object):
    """A class for handling the data retrieval."""

    def __init__(self, loop, session, api_key, source="USD", quote=None):
        """Initialize the connection to the currencylayer API."""
        self._loop = loop
        self._quote = quote
        self._session = session
        self._timestamp = self._quotes = None
        self.data = {}
        self.source = source
        self.valid = self.free = None
        self.parameters = {
            "source": self.source,
            "access_key": api_key,
            "format": 1,
        }

    async def get_data(self):
        """Retrieve the data from currencylayer."""
        try:
            with async_timeout.timeout(5, loop=self._loop):
                response = await self._session.get(_RESOURCE, params=self.parameters)

            _LOGGER.debug("Response from CurrencyLayer API: %s", response.status)

            self.data = await response.json()
            _LOGGER.debug(self.data)

            if self.data["success"] is False:
                self.valid = False
                raise exceptions.CurrencyLayerAuthenticationError(
                    "API key is not valid"
                )

        except (asyncio.TimeoutError, aiohttp.ClientError):
            _LOGGER.error("Can not load data from currencylayer API")
            raise exceptions.CurrencyLayerConnectionError()

        self._quotes = {
            key.replace(self.source, ""): round(value, 4)
            for key, value in self.data["quotes"].items()
        }

        if self.data["success"] is False:
            if self.data["error"]["code"] == 101:
                self.valid = False
            if self.data["error"]["code"] == 105:
                self.free = True
            if self.data["error"]["code"] == 103:
                raise exceptions.CurrencyLayerConnectionError(
                    self.data["error"]["info"].split(".")[0]
                )
        else:
            self.valid = True

    @property
    def timestamp(self):
        """Return the timestamp of the quotes."""
        return self.data["timestamp"]

    @property
    def quote(self):
        """Return the requested quote."""
        if self._quote is not None:
            return self._quotes[self._quote]
        else:
            return self._quotes

    @property
    def quotes(self):
        """Return the available quotes."""
        return self._quotes

    async def validate_api_key(self):
        """Return the validity of the API key."""
        return self.valid

    async def check_free_plan(self):
        """Return True if free plan (only USD as source currency allowed)."""
        return self.free

    async def supported_currencies(self):
        """Return supported currencies."""
        return list(self._quotes.keys())
