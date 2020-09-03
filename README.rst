python-currencylayer
====================

Python API for interacting with `currencylayer <https://currencylayer.com/>`_.
At the moment only the consumption of data is supported.

This module is not official, developed, supported or endorsed by currencylayer.

Installation
------------

The module is available from the `Python Package Index <https://pypi.python.org/pypi>`_.

.. code:: bash

    $ pip3 install aiocurrencylayer

Usage
-----

The file ``example.py`` contains an example about how to use this module.

Basically it's just a wrapper. Enter your currencylayer API key and the
currency you want a quote for. Free subscriptions only support USD as source
currency.

.. code:: bash

    $ python3 example.py

Development
-----------

For development is recommended to use a ``venv``.

.. code:: bash

    $ python3 -m venv .
    $ source bin/activate
    $ python3 setup.py develop

License
-------

``python-currencylayer`` is licensed under MIT, for more details check
LICENSE.
