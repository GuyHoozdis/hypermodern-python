# https://nox.thea.codes/en/stable/config.html#modifying-nox-s-behavior-in-the-noxfile
import nox

nox.options.sessions = "lint", "tests"


PYTHON_VERSIONS = ["3.12", "3.11", "3.10", "3.9", "3.8"]
LINT_TARGETS = ["src/", "tests/", "noxfile.py"]


# TODO: Do I need to keep this if I am using flake8-black?
@nox.session(python="3.11")
def black(session):
    args = session.posargs or LINT_TARGETS
    session.install("black")
    session.run("black", *args)


# TODO: Does flake8 behave differently under different python versions?
# - Should this be running for different python versions or can it be just one?
# - Can I dynamically select the python version being used by the dev and just use that instead of hardcode?
# @nox.session(python=PYTHON_VERSIONS)
@nox.session(python="3.11")
def lint(session):
    args = session.posargs or LINT_TARGETS
    session.install("flake8", "flake8-black")
    session.run("flake8", *args)


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)
