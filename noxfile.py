import nox


PYTHON_VERSIONS = ["3.12", "3.11", "3.10", "3.9", "3.8"]


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)
