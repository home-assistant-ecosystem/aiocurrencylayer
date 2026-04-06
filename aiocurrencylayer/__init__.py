"""Wrapper for interacting with the currencylayer API."""
import logging
from typing import Any

import httpx

from . import exceptions

_LOGGER = logging.getLogger(__name__)
_RESOURCE = "http://apilayer.net/api/live"


class CurrencyLayer(object):
    """A class for handling the data retrieval."""

    def __init__(
        self, api_key: str, source: str = "USD", quote: str | None = None
    ) -> None:
        """Initialize the connection to the currencylayer API."""
        self._quote: str | None = quote
        self._timestamp: int | None = None
        self._quotes: dict[str, float] | None = None
        self.data: dict[str, Any] = {}
        self.source: str = source
        self.valid: bool | None = None
        self.free: bool | None = None
        self.parameters: dict[str, Any] = {
            "source": self.source,
            "access_key": api_key,
            "format": 1,
        }

    async def get_data(self) -> None:
        """Retrieve the data from currencylayer."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(str(_RESOURCE), params=self.parameters)
        except httpx.ConnectError:
            raise exceptions.CurrencyLayerConnectionError()

        if response.status_code == httpx.codes.OK:
            _LOGGER.debug(response.json())
            try:
                self.data = response.json()
            except TypeError:
                _LOGGER.error("Can not load data from currencylayer API")
                raise exceptions.CurrencyLayerConnectionError(
                    "Unable to get the data from currencylayer API"
                )

        if self.data["success"] is False:
            if self.data["error"]["code"] == 101:
                self.valid = False
                raise exceptions.CurrencyLayerAuthenticationError(
                    "API key is not valid"
                )
            if self.data["error"]["code"] == 105:
                raise exceptions.CurrencyLayerError(
                    "Your subscription only support USD (free plan)"
                )
            if self.data["error"]["code"] == 103:
                raise exceptions.CurrencyLayerConnectionError(
                    self.data["error"]["info"].split(".")[0]
                )
        else:
            self.valid = True

        self._quotes = {
            key.replace(self.source, ""): round(value, 4)
            for key, value in self.data["quotes"].items()
        }

    @property
    def timestamp(self) -> int:
        """Return the timestamp of the quotes."""
        return self.data["timestamp"]

    @property
    def quote(self) -> float | dict[str, float] | None:
        """Return the requested quote."""
        if self._quote is not None:
            assert self._quotes is not None
            return self._quotes[self._quote]
        else:
            return self._quotes

    @property
    def quotes(self) -> dict[str, float] | None:
        """Return the available quotes."""
        return self._quotes

    @property
    def validate_api_key(self) -> bool | None:
        """Return the validity of the API key."""
        return self.valid

    @property
    def supported_currencies(self) -> list[str]:
        """Return the supported currencies."""
        assert self._quotes is not None
        return list(self._quotes.keys())
