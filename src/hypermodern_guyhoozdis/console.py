"""Command-line interface."""
# TODO: The documentation generated for this module in the reference.rst is not helpful.  Either
# add some useful context or find a way to remove that from being displayed in the docs.

import textwrap

import click

from . import __version__, wikipedia


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
def main(language: str) -> int:
    """The Hypermodern Python Project."""
    page = wikipedia.random_page(language=language)

    click.secho(page.title, fg="green")
    click.echo(textwrap.fill(page.extract))

    return 0


# TODO: Don't really need this and a __main__.py file.
if __name__ == "__main__":
    import sys

    sys.exit(
        main(sys.argv[1:])
    )
