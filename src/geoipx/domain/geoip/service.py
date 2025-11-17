from datetime import datetime
import requests
from pathlib import Path
import os
from geoipx.utils.output_types import OutputType
from geoipx.utils.parsers import to_json, to_xml, to_csv
from geoipx.exceptions.output_format_exceptions import OutputFormatError

class GeoIPService:

    def lookup_ip(self, ip: str, output_format: OutputType, output_dir: str = os.getcwd()) -> str:
        res = requests.get(f"https://ipwho.is/{ip}").json()

        flat_res = {k: v for k, v in res.items() if not isinstance(v, dict)}

        if output_format == OutputType.JSON:
            content = to_json(flat_res)
        elif output_format == OutputType.XML:
            content = to_xml(flat_res)
        elif output_format == OutputType.CSV:
            content = to_csv(flat_res)
        else:
            raise OutputFormatError.from_format(output_format, "Unsupported output format", "Please use JSON, XML, or CSV.")

        if output_dir:
            dir_path = Path(output_dir).expanduser()
            
            if dir_path.exists() and not dir_path.is_dir():
                raise OutputFormatError.from_invalid_directory("Output path must be a directory, not a file. Please provide a directory path.")

            dir_path.mkdir(parents=True, exist_ok=True)
            filename = f"geoipx_lookup_{datetime.now().strftime('%Y%m%d_%H%M%S')}{output_format.output_extension}"
            file_path = dir_path / filename
            file_path.write_text(content, encoding="utf-8")

            return f"Output saved to {file_path}"

        return content
       