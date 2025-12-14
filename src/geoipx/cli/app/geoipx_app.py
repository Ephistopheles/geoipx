import typer

from geoipx.cli.callbacks.global_callback import global_callback
from geoipx.cli.commands.lookup.geoipx_lookup_command import geoipx_lookup_command

def create_app() -> typer.Typer:
    """Create an instance of the GeoIPX app."""
    geoipx_app = typer.Typer(
        no_args_is_help=False,
        add_completion=False,
        add_help_option=False,
        callback=global_callback,
        invoke_without_command=True,
        help="GeoIPX - A CLI tool for GeoIP lookups",
    )

    geoipx_app.add_typer(geoipx_lookup_command)

    return geoipx_app

app = create_app()
