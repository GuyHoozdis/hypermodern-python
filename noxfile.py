import tempfile

import nox


nox.options.sessions = "lint", "tests"


PYTHON_VERSIONS = ["3.12", "3.11", "3.10", "3.9", "3.8"]
LINT_TARGETS = ["src/", "tests/", "./noxfile.py"]


# !!! LEFT OFF HERE !!!
# See my notes, in Evernote, about the "Managing Dependencies in Nox Session with Poetry" section
# of Hypermodern Python.
#   https://cjolowicz.github.io/posts/hypermodern-python-03-linting/#managing-dependencies-in-nox-sessions-with-poetry


# TODO: Make --without-hashes an argument to this function and then it can be used for safety too.
def install_with_constraints(session, *args, **kwargs):
    #with tempfile.NamedTemporaryFile() as requirements:
    with tempfile.NamedTemporaryFile() as constraints:
        session.run(
            "poetry",
            "export",
            "--with",
            "dev",
            #"--format=requirements.txt",
            "--format=constraints.txt",
            f"--output={constraints.name}",
            external=True,
        )
        session.install("--no-deps", f"--constraint={constraints.name}", *args, **kwargs)


# TODO: Add poetry-plugin-export to project to avoid breaking in the future when the export command is removed.
# TODO: Switch to `safety scan` instead of `check`
@nox.session(python="3.11")
def safety(session):
    session.install("safety")
    if session.posargs:
        session.run("safety", *session.posargs)
        return

    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


# TODO: Do I need to keep this if I am using flake8-black?
@nox.session(python="3.11")
def black(session):
    args = session.posargs or LINT_TARGETS
    # session.install("black")
    install_with_constraints(session, "black")
    session.run("black", *args)


# TODO: Replace flake8-import-order with flake8-isort or pre-commit.
# TODO: Does flake8 behave differently under different python versions?
# - Should this be running for different python versions or can it be just one?
# - Can I dynamically select the python version being used by the dev and just use that instead of hardcode?
# @nox.session(python=PYTHON_VERSIONS)
@nox.session(python="3.11")
def lint(session):
    args = session.posargs or LINT_TARGETS
    session.install(
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order",
    )
    session.run("flake8", *args)


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)
