"""The Hypermodern GuyHoozdis Main Entrypoint."""

# This file is excluded from coverage by the configuration in pyproject.toml.  That
# is acceptable because the logic in this module is simple.  If more complex logic is
# added here, then coverage should be re-enabled.  Remove "__main__.py" from the
# "tool.coverage.run" section in pyproject.toml.
import sys

from hypermodern_guyhoozdis import console


rc = console.main(sys.argv[1:])
sys.exit(rc)
