import typer
from rich.panel import Panel
from rich import print as rich_print
from geoipx import __version__, __app_name__

def global_callback(
    ctx: typer.Context,
    geoipx_version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show the version of GeoIPX.",
        is_eager=True
    ),
    geoipx_help: bool = typer.Option(
        False,
        "--help",
        "-h",
        help="Show the help of GeoIPX.",
        is_eager=True
    )
) -> None:
    """Global callback for GeoIPX."""
    if geoipx_version:
        rich_print(Panel(f"{__app_name__} version: {__version__}", title=f"[bold green]{__app_name__} Info", title_align="left", border_style="green"))
        raise typer.Exit()
    if geoipx_help or not ctx.invoked_subcommand:
        rich_print(Panel(f"{__app_name__} help: {__version__}", title=f"[bold green]{__app_name__} Info", title_align="left", border_style="green"))
        raise typer.Exit()
