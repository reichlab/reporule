"""Create the reichlab CLI."""

import structlog
from rich.console import Console
from rich.panel import Panel

logger = structlog.get_logger()


def main():
    """reichlab starting point."""
    logger.info("starting reichlab...")

    console = Console()
    console.print(
        Panel(
            ":tada: Hello from the reichlab Python package!",
            border_style="green",
            expand=False,
            padding=(1, 4),
            subtitle="[italic]created by pyprefab[/italic]",
            subtitle_align="right",
            title="reichlab",
            title_align="left",
        )
    )


if __name__ == "__main__":
    main()
