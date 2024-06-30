import textwrap

import click

from . import __version__, wikipedia


# !!! LEFT OFF HERE !!!
#   https://cjolowicz.github.io/posts/hypermodern-python-04-typing/
# I may need to address Issue #4 (the install_with_constraints issue) before I can move
# forward.  Alternatively, I could start ignoring things like `click` temporarily and
# come back to fix them later.  Or I could install the whole poetry environment before
# running mypy.
@click.command()
@click.option(
    "--language",
    "-l",
    default="en",
    help="Language edition of Wikipedia",
    metavar="LANG",
    show_default=True,
)
@click.version_option(version=__version__)
def main(language: str) -> None:
    """The Hypermodern Python Project"""
    page = wikipedia.random_page(language=language)

    click.secho(page.title, fg="green")
    click.echo(textwrap.fill(page.extract))
