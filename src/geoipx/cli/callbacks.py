import typer
from geoipx import __version__
from rich.panel import Panel
from rich import print as rich_print

def global_callback(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show the version of GeoIPX.",
        is_eager=True,
    ),
):
    if version:
        rich_print(Panel(f"GeoIPX version: {__version__}", title="[bold green]GeoIPX Info", title_align="left", border_style="green"))
        raise typer.Exit()