"""Exceptions for wrapper to interact with the currencylayer API."""


class CurrencyLayerError(Exception):
    """General currencylayer Error exception occurred."""


class CurrencyLayerConnectionError(CurrencyLayerError):
    """When a connection error is encountered."""


class CurrencyLayerAuthenticationError(CurrencyLayerError):
    """When a authentication error is encountered."""


class CurrencyLayerNoDataAvailable(CurrencyLayerError):
    """When no data is available."""
