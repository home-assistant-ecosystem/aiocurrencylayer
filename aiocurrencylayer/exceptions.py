"""Exceptions for wrapper to interact with the currencylayer API."""


class CurrencyLayerError(Exception):
    """General currencylayer Error exception occurred."""

    pass


class CurrencyLayerConnectionError(CurrencyLayerError):
    """When a connection error is encountered."""

    pass


class CurrencyLayerAuthenticationError(CurrencyLayerError):
    """When a authentication error is encountered."""

    pass


class CurrencyLayerNoDataAvailable(CurrencyLayerError):
    """When no data is available."""

    pass
