"""Nox sessions."""

# https://nox.thea.codes/en/stable/config.html#modifying-nox-s-behavior-in-the-noxfile
import nox
from nox.sessions import Session

nox.options.sessions = "lint", "mypy", "tests", "xdoctests", "docs"


DEFAULT_PYTHON_VERSION = "3.11"
SUPPORTED_PYTHON_VERSIONS = ["3.12", "3.11", "3.10", "3.9", "3.8"]
SOURCE_CODE_TARGETS = ["src/", "tests/", "./noxfile.py", "docs/conf.py"]


package = "hypermodern_python"


# TODO: Return to reimplement this.  For now, just make note the signature.
# def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
#     pass


@nox.session(python=DEFAULT_PYTHON_VERSION)
def typeguard(session: Session) -> None:
    """Runtime type checking using Typeguard."""
    args = session.posargs or ["-m", "not e2e"]
    session.run("poetry", "install", "--only", "main", external=True)

    session.install("pytest", "pytest-mock", "typeguard")
    session.run("pytest", "--typeguard-packages={package}", *args)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def mypy(session: Session) -> None:
    """Static type checking using mypy."""
    args = session.posargs or SOURCE_CODE_TARGETS
    session.install("mypy")

    # XXX: Doing this to workaround the install_with_constraints issue.
    session.run("poetry", "install", "--no-root", external=True)
    session.install("types-requests")

    session.run("mypy", *args)


# TODO: Do I need to keep this if I am using flake8-black?
# A: Maybe.  When flake8-black runs it may report an issue without enough detail to fix it.  In that
#    case, I've been running `nox -s black` to resolve the issue.  However, there seems to be a
#    difference in the configuration of the two.  I haven't looked into that yet.
@nox.session(python=DEFAULT_PYTHON_VERSION)
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or SOURCE_CODE_TARGETS
    session.install("black")
    session.run("black", *args)


# TODO: Replace flake8-import-order with flake8-isort or pre-commit.
# TODO: Does flake8 behave differently under different python versions?
# - Should this be running for different python versions or can it be just one?
# - Can I dynamically select the python version being used by the dev and just use that instead of hardcode?
# @nox.session(python=PYTHON_VERSIONS)
@nox.session(python="3.11")
def lint(session: Session) -> None:
    """Lint using flake8 and plugins."""
    args = session.posargs or SOURCE_CODE_TARGETS
    session.install(
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
        "darglint",
    )
    session.run("flake8", *args)


@nox.session(python=SUPPORTED_PYTHON_VERSIONS)
def tests(session: Session) -> None:
    """Run the test suite."""
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


# Alternatively, this could be done as a pytest plugin.
@nox.session(python=SUPPORTED_PYTHON_VERSIONS)
def xdoctests(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    session.run("poetry", "install", "--only", "main", external=True)
    session.install("xdoctest")
    session.run("python", "-m", "xdoctest", package, *args)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def docs(session: Session) -> None:
    """Build the documentation."""
    # TODO: This doesn't need the main dependencies nor most of the other dev dependencies.  Move
    # the required packages sphinx and sphinx-autodoc-typehints into their own dependency group and
    # then use the --only switch to install.
    session.run("poetry", "install", "--no-root", external=True)
    session.run("sphinx-build", "docs", "docs/_build")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def coverage(session: Session) -> None:
    """Upload coverage data."""
    session.install("coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
