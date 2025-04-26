"""Command line interface entrypoint for the reporule package."""

from reporule.logging import setup_logging
from reporule.main import app

# Set up logging
setup_logging()

if __name__ == "__main__":
    app()
