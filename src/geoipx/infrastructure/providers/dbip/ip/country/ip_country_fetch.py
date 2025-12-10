import io
import gzip
import requests
from pathlib import Path
import datetime
from geoipx.infrastructure.db_geoipx.connection.connection import GeoIPXDataBase

def _get_url_date():
    current_date = datetime.datetime.now()
    return f"{current_date.year}-{current_date.month}"

DBIP_IP_COUNTRY_URL = f"https://download.db-ip.com/free/dbip-country-lite-{_get_url_date()}.csv.gz"

class DBIPCountryIPFetcher:

    TMP_DIR = Path.home() / ".geoipx" / "tmp" / "dbip"
    
    def fetch(self):
        try:
            compressed = self._download()
            decompressed = self._descompress(compressed)
            self._load_into_duckdb(decompressed)
        except Exception as e:
            raise RuntimeError("Failed to fetch and process data") from e
    
    def _download(self) -> bytes:
        try:
            res = requests.get(DBIP_IP_COUNTRY_URL, timeout=30)
            res.raise_for_status()
            return res.content
        except requests.exceptions.Timeout as e:
            raise TimeoutError(f"Request to {DBIP_IP_COUNTRY_URL} timed out") from e
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to download from {DBIP_IP_COUNTRY_URL}") from e
        
    def _descompress(self, data: bytes) -> bytes:
        try:
            with gzip.GzipFile(fileobj=io.BytesIO(data)) as gz_file:
                file = gz_file.read()
                if not file:
                    raise ValueError("GZ file is empty")
                return file
        except OSError as e:
            raise ValueError("Invalid GZ file") from e
        
    def _load_into_duckdb(self, csv_bytes: bytes):
        self.TMP_DIR.mkdir(parents=True, exist_ok=True)
        tmp_csv_path = self.TMP_DIR / f"dbip_ip_country_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

        tmp_csv_path.write_bytes(csv_bytes)

        conn = GeoIPXDataBase().conn

        schema_base = Path(__file__).parents[4] / "db_geoipx" / "schema" / "ip" / "dbip" / "country"

        create_v4_sql = (schema_base / "v4" / "dbip_country_ip_v4.sql").read_text()
        create_v6_sql = (schema_base / "v6" / "dbip_country_ip_v6.sql").read_text()

        conn.execute(create_v4_sql)
        conn.execute(create_v6_sql)

        loaders_base = Path(__file__).parents[4] / "db_geoipx" / "queries" / "loaders" / "dbip" / "ip" / "country"

        loader_v4 = (loaders_base / "v4" / "dbip_loader_country_ip_v4.sql").read_text().replace("{csv_path}", str(tmp_csv_path))
        loader_v6 = (loaders_base / "v6" / "dbip_loader_country_ip_v6.sql").read_text().replace("{csv_path}", str(tmp_csv_path))

        conn.execute(loader_v4)
        conn.execute(loader_v6)
        
        tmp_csv_path.unlink()
