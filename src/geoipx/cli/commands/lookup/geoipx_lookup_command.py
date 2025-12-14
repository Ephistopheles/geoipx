import typer
from rich.panel import Panel
from rich import print as rich_print
from geoipx.utils.output_types import OutputType
from geoipx.domain.geoip.service import GeoIPService
from geoipx.exceptions.ip_exceptions import InvalidIPError
from geoipx.domain.validation.ip_validator import validate_ip
from geoipx.exceptions.output_format_exceptions import OutputFormatError

geoipx_lookup_command = typer.Typer()

@geoipx_lookup_command.command("lookup")
def lookup(
    ip: str = typer.Argument(
        ...,
        help="The IP address to lookup.",
    ),
    json: bool = typer.Option(
        False,
        "--json",
        "-j",
        help="Output result in JSON format.",
        is_eager=True,
    ),
    xml: bool = typer.Option(
        False,
        "--xml",
        "-x",
        help="Output result in XML format.",
        is_eager=True,
    ),
    csv: bool = typer.Option(
        False,
        "--csv",
        "-c",
        help="Output result in CSV format.",
        is_eager=True,
    ),
    output_dir: str = typer.Option(
        None,
        "--output",
        "-o",
        help="Directory path to save the output. If not provided, uses the current working directory.",
        is_eager=True,
    ),
):
    """
    Lookup the geographical information for a given IP address.
    """
    try:
        validated_ip = validate_ip(ip)
    except InvalidIPError:
        raise typer.Exit(code=1)

    output_format = OutputType.JSON if json else OutputType.XML if xml else OutputType.CSV if csv else OutputType.JSON

    try:
        result = GeoIPService().lookup_ip(validated_ip, output_format, output_dir)
    except OutputFormatError:
        raise typer.Exit(code=1)

    rich_print(Panel(result, title="[bold green]GeoIPX Result", title_align="left", border_style="green"))
    