# The Hypermodern Python Project

[![Tests](https://github.com/GuyHoozdis/hypermodern-python/workflows/Tests/badge.svg)](https://github.com/GuyHoozdis/hypermodern-python/actions?workflow=Tests)
[![Codecov](https://codecov.io/gh/GuyHoozdis/hypermodern-python/branch/master/graph/badge.svg)](https://codecov.io/gh/GuyHoozdis/hypermodern-python)


A template based on ["The Hypermodern Python Project"][hypermodern-python].


## Quick Start

_Note: Assumes you have poetry, nox, and the required python versions installed. See the [Development Environment Setup](#development-environment-setup) section below for instructions on setting up the
required environment._

Run the following commands from the root of the repo.


### Initialize the virtual environment

Construct poetry's virtual environment.

```bash
$ poetry install
```

If you have made changes to the dependencies, then you must update the lock file.

```bash
$ poetry lock
$ poetry install
```


### Run the full test suite

```bash
$ nox
#
# ... snip...
#
nox > Ran multiple sessions:
nox > * tests-3.12: success
nox > * tests-3.11: success
nox > * tests-3.10: success
nox > * tests-3.9: success
nox > * tests-3.8: success
```

Reuse existing virtual environments with the `-r/--reuse-existing-virtualenvs` switch to speed up re-running the test suite.

```bash
$ nox -r
```


### Run all tests for a single python version

List the available sessions with `-l/--list` and select one or more with the `-s/--session` switch.

```bash
$ nox -l
Sessions defined in /<path>/<to>/<repo>/hypermodern-python/noxfile.py:

* tests-3.12
* tests-3.11
* tests-3.10
* tests-3.9
* tests-3.8

$ nox -rs tests-3.11 tests-3.10
#
# ... snip...
#
nox > Ran multiple sessions:
nox > * tests-3.11: success
nox > * tests-3.10: success
```


### Run all tests in a single module

```bash
$ nox -rs tests-3.11 -- tests/test_console.py
#
# ... snip...
#
tests/test_console.py ....
#
# ... snip...
#
nox > Session tests-3.11 was successful.
```


### Run a specific tests from a specific module

```bash
$ nox -rs tests-3.11 -- tests/test_console.py::test_main_fails_on_request_error
#
# ... snip...
#
tests/test_console.py .
#
# ... snip...
#
nox > Session tests-3.11 was successful.
```


### Run the debugger when a breakpoint is hit

This example is a demonstration of passing arbitrary arguments to `pytest` which is being run by `nox`, not an assertion that this is the best way to run the debugger.

See [TODO: Get a reference to docs] for more information about setting breakpoints.

```bash
$ nox -rs tests-3.11 -- -s --pdbcls=IPython.terminal.debugger:TerminalPdb tests/test_console.py::test_main_fails_on_request_error

tests/test_console.py Python 3.11.9 (main, Jun 12 2024, 14:42:40) [Clang 14.0.0 (clang-1400.0.29.202)]
Type 'copyright', 'credits' or 'license' for more information
IPython 8.25.0 -- An enhanced Interactive Python. Type '?' for help.
ipdb> ll
     37 def test_main_fails_on_request_error(runner, mock_reqeusts_get):
     38     mock_reqeusts_get.side_effect = Exception("Boom")
     39     result = runner.invoke(console.main)
     40     breakpoint()
---> 41     assert result.exit_code == 1
     42     assert "Boom" == str(result.exception)

ipdb> c

#
# ... snip...
#
nox > Session tests-3.11 was successful.
```


### Run the end-to-end tests

The end-to-end tests are marked with `pytest.markers.e2e` and can be invoked by the command below.  By default tests with the `e2e` marker will not be executed.

```bash
$ nox -rs tests-3.11 -- -m e2e
```


### Build Documentation

```bash
$ nox -rs docs
$ open docs/_build/index.html
```


## Development Environment Setup

TODO: Write steps to setup development environment.

1. Install `pyenv`
1. Install python versions
1. Install `poetry`
1. Install `nox`
1. Verify environment setup


## Publish Package

From the [Poetry docs][poetry-config-credentials]


```
$ poetry source add --priority explicit testpypi https://test.pypi.org/simple/
$ poetry config pypi-token.testpypi <your-test-pypi-token>
$ poetry config pypi-token.pypi <your-pypi-token>
```

Verify it is in the system keyring

```
$ keyring get poetry-repository-testpypi __token__
pypi-llsijlsdjlsjlsij...

$ keyring get poetry-repository-pypi __token__
pypi-llsijlsdjlsjlsij...
```

Build and publish

```
$ poetry build
$ poetry publish -r testpypi
$ poetry publish
```

!!!: Publishing to testpypi is not working for me yet.  Publishing to regular PyPi does.  I'm not sure why yet.


# Resources

1. [The Hypermodern Python Project articles][hypermodern-python]
1. [The Hypermodern Python Project GitHub Repo][hypermodern-python-github]
1. [Poetry: Configuring Credentials][poetry-config-credentials]


[hypermodern-python]: https://cjolowicz.github.io/posts/hypermodern-python-01-setup/
[hypermodern-python-github]: https://github.com/cjolowicz/hypermodern-python
[poetry-config-credentials]: https://python-poetry.org/docs/repositories/#configuring-credentials
