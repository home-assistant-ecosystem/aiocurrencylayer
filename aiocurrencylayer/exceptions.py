"""Exceptions for wrapper to interact with the CurrencyLayer API."""


class CurrencyLayerError(Exception):
    """General CurrencyLayer Error exception occurred."""

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
