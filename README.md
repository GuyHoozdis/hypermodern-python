# The Hypermodern Python Project

[![Tests](https://github.com/GuyHoozdis/hypermodern-python/workflows/Tests/badge.svg)](https://github.com/GuyHoozdis/hypermodern-python/actions?workflow=Tests)
[![Codecov](https://codecov.io/gh/GuyHoozdis/hypermodern-python/branch/master/graph/badge.svg)](https://codecov.io/gh/GuyHoozdis/hypermodern-python)


A template based on ["The Hypermodern Python Project"][hypermodern-python].


## Quick Start

_Note: Assumes you have poetry, nox, and the required python versions installed. See the [Development Environment Setup](#development-environment-setup) section below for instructions on setting up the
required environment._

Run the following commands from the root of the repo.


### initialize the virtual environment

Construct poetry's virtual environment.

```bash
$ poetry install
```

If you have made changes to the dependencies, then you must update the lock file.

```bash
$ poetry lock
$ poetry install
```


### run the full test suite

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


### run all tests for a single python version

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


### run all tests in a single module

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


### run a specific tests from a specific module

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


### run the debugger when a breakpoint is hit

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


### run the end-to-end tests

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


# Resources

1. [The Hypermodern Python Project articles][hypermodern-python]
1. [The Hypermodern Python Project GitHub Repo][hypermodern-python-github]


[hypermodern-python]: https://cjolowicz.github.io/posts/hypermodern-python-01-setup/
[hypermodern-python-github]: https://github.com/cjolowicz/hypermodern-python
