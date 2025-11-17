import typer
from geoipx.cli.callbacks import global_callback
from geoipx.cli.geoip_commands import geoip_commands

app = typer.Typer(
    callback=global_callback,
    help="GeoIPX - A CLI tool for GeoIP lookups",
    no_args_is_help=True,
    invoke_without_command=True
)

app.add_typer(geoip_commands)
