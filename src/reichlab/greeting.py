"""Command for greetings."""

import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer()


@app.command()
def greeting():
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
