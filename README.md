
# GeoIPX

GeoIPX is a command-line tool (CLI) for performing GeoIP lookups on public IP addresses. It allows you to obtain geographic information in JSON, XML, or CSV formats, and save the results to a specified directory.

## Installation

Requirements:
- Python 3.12 or higher
- [Poetry](https://python-poetry.org/) for dependency management

Install dependencies by running:

```bash
poetry install
```

## Usage

Basic help:

```bash
poetry run python -m geoipx --help
```

To lookup information for an IP:

```bash
poetry run python -m geoipx lookup 8.8.8.8 --json
```

Format options:
- `--json` for JSON output
- `--xml` for XML output
- `--csv` for CSV output

You can save the result to a specific directory using `--output`:

```bash
poetry run python -m geoipx lookup 8.8.8.8 --json --output ./results
```

## Author

Ephistopheles (<rjohanamed@gmail.com>)
