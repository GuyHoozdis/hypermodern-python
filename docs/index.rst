The Hypermodern GuyHoozdis Project
==================================

.. toctree::
   :hidden:
   :maxdepth: 1

   license
   reference


My implementation of the
`Hypermodern Python <https://https://cjolowicz.github.io/posts/hypermodern-python-01-setup/>`_
project article series.
The command-line interface prints random facts to your console,
using the `Wikipedia API <https://en.wikipedia.org/api/rest_v1/#/>`_.


Command Line interface
----------------------

Without any parameters,
the CLI will use the default langage configured
and call the Wikipedia API to return a random page.

Passing ``--help`` will display the application usage.

.. code-block:: console

   $ hypermodern-guyhoozdis [OPTIONS]

.. option:: -l/--language <language>

   The Wikipedia language edition,
   as identified by its subdomain on
   `wikipedia.org <https://www.wikipedia.org/>`_.
   By default, the English Wikipedia is selected.

.. option:: --version

   Display the version and exit.

.. option:: --help

   Display a short usage message and exit.


Quick Start
-----------

To install the Hypermodern GuyHoozdis package,
run this command in your terminal:

.. code-block:: console

   $ pip -m venv sandbox
   $ source sandbox/bin/activate
   $ pip install hypermodern-guyhoozdis


Now you can use the CLI.


The CLI can be executed natively...

.. code-block:: console

   $ hypermodern-guyhoozdis --language=de


... or as a module passed to the python interpreter.

.. code-block:: console

   $ python -m hypermodern-guyhoozdis --language=fr


Alternatively, you can use the package in your own code.

.. code-block:: python

   >>> from hypermodern_guyhoozdis import wikipedia
   >>> page = wikipedia.random_page()
   >>> page.title
   'VMI Keydets baseball'
   >>> len(page.extract)
   384
