import io
import zipfile
import requests
from pathlib import Path
from datetime import datetime
from geoipx.infrastructure.db_geoipx.connection.connection import GeoIPXDataBase

TOKEN_IP2LOCATION = "LbLuGQmzPOLDBiQ4RpY2bb5kAam7oI8pcU0JyoWfa3qhtu4XItCRIahrLwgERYx4"

DATABASE_CODE_IP2LOCATION = "DB11LITECSV"

IP2LOCATION_V4_URL = f"https://www.ip2location.com/download/?token={TOKEN_IP2LOCATION}&file={DATABASE_CODE_IP2LOCATION}"

class IP2LocationIPV4Fetcher:

    TMP_DIR = Path.home() / ".geoipx" / "tmp" / "ip2location"

    def fetch(self):
        try:
            compressed = self._download()
            decompressed = self._descompress(compressed)
            self._load_into_duckdb(decompressed)
        except Exception as e:
            raise RuntimeError("Failed to fetch and process data") from e
    
    def _download(self) -> bytes:
        try:
            res = requests.get(IP2LOCATION_V4_URL, timeout=30)
            res.raise_for_status()
            return res.content
        except requests.exceptions.Timeout as e:
            raise TimeoutError(f"Request to {IP2LOCATION_V4_URL} timed out") from e
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to download from {IP2LOCATION_V4_URL}") from e
        
    def _descompress(self, data: bytes) -> bytes:
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                files = z.namelist()

                if not files:
                    raise ValueError("ZIP file is empty")

                csv_files = [f for f in files if f.lower().endswith('.csv')]
                
                if not csv_files:
                    raise ValueError("ZIP file does not contain a CSV file")
                
                return z.open(csv_files[0], "r").read()
        except zipfile.BadZipFile as e:
            raise ValueError("Invalid ZIP file") from e

    def _load_into_duckdb(self, csv_bytes: bytes):
        self.TMP_DIR.mkdir(parents=True, exist_ok=True)
        tmp_csv_path = self.TMP_DIR / f"ip2location_v4_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

        tmp_csv_path.write_bytes(csv_bytes)

        conn = GeoIPXDataBase().conn

        schema_base = Path(__file__).parents[4] / "db_geoipx" / "schema" / "ip" / "ip2location"

        create_v4_sql = (schema_base / "v4" / "ip2location_ip_v4.sql").read_text()

        conn.execute(create_v4_sql)

        loaders_base = Path(__file__).parents[4] / "db_geoipx" / "queries" / "loaders" / "ip2location" / "ip"

        loader_v4 = (loaders_base / "v4" / "ip2location_loader_ip_v4.sql").read_text().replace("{csv_path}", str(tmp_csv_path))

        conn.execute(loader_v4)
        
        tmp_csv_path.unlink()
