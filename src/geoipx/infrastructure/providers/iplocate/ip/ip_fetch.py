import io
import zipfile
import requests
from pathlib import Path
from datetime import datetime
from geoipx.infrastructure.db_geoipx.connection.connection import GeoIPXDataBase

IPLOCATE_IP_URL = "https://github.com/iplocate/ip-address-databases/raw/refs/heads/main/ip-to-country/ip-to-country.csv.zip"

class IPLocateIPFetcher:

    TMP_DIR = Path.home() / ".geoipx" / "tmp" / "iplocate"
    
    def fetch(self):
        try:
            compressed = self._download()
            decompressed = self._descompress(compressed)
            self._load_into_duckdb(decompressed)
        except Exception as e:
            raise RuntimeError("Failed to fetch and process data") from e
    
    def _download(self) -> bytes:
        try:
            res = requests.get(IPLOCATE_IP_URL, timeout=30)
            res.raise_for_status()
            return res.content
        except requests.exceptions.Timeout as e:
            raise TimeoutError(f"Request to {IPLOCATE_IP_URL} timed out") from e
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to download from {IPLOCATE_IP_URL}") from e
        
    def _descompress(self, data: bytes) -> bytes:
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                files = z.namelist()

                if not files:
                    raise ValueError("ZIP file is empty")

                with z.open(files[0], "r") as f:
                    return f.read()
        except zipfile.BadZipFile as e:
            raise ValueError("Invalid ZIP file") from e

    def _load_into_duckdb(self, csv_bytes: bytes):
        self.TMP_DIR.mkdir(parents=True, exist_ok=True)
        tmp_csv_path = self.TMP_DIR / f"iplocate_ip_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

        tmp_csv_path.write_bytes(csv_bytes)

        conn = GeoIPXDataBase().conn

        schema_base = Path(__file__).parents[3] / "db_geoipx" / "schema" / "ip" / "iplocate" / "country"

        create_v4_sql = (schema_base / "v4" / "iplocate_country_ip_v4.sql").read_text()
        create_v6_sql = (schema_base / "v6" / "iplocate_country_ip_v6.sql").read_text()

        conn.execute(create_v4_sql)
        conn.execute(create_v6_sql)

        loaders_base = Path(__file__).parents[3] / "db_geoipx" / "queries" / "loaders" / "iplocate" / "ip" / "country"

        loader_v4 = (loaders_base / "v4" / "iplocate_loader_country_ip_v4.sql").read_text().replace("{csv_path}", str(tmp_csv_path))
        loader_v6 = (loaders_base / "v6" / "iplocate_loader_country_ip_v6.sql").read_text().replace("{csv_path}", str(tmp_csv_path))

        conn.execute(loader_v4)
        conn.execute(loader_v6)
        
        tmp_csv_path.unlink()
