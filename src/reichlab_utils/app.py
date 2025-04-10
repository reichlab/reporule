import structlog
from rich.console import Console
from rich.panel import Panel

from reichlab_utils.logging import setup_logging

setup_logging()
logger = structlog.get_logger()


def main():
    """reichlab_utils starting point."""
    logger.info('starting reichlab_utils...')

    console = Console()
    console.print(
        Panel(
            ':tada: Hello from the reichlab_utils Python package!',
            border_style='green',
            expand=False,
            padding=(1, 4),
            subtitle='[italic]created by pyprefab[/italic]',
            subtitle_align='right',
            title='reichlab_utils',
            title_align='left',
        )
    )


if __name__ == '__main__':
    main()

