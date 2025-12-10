import io
import gzip
import requests
from pathlib import Path
import datetime
from geoipx.infrastructure.db_geoipx.connection.connection import GeoIPXDataBase

def _get_url_date():
    current_date = datetime.datetime.now()
    return f"{current_date.year}-{current_date.month}"

DBIP_IP_URL = f"https://download.db-ip.com/free/dbip-country-lite-{_get_url_date()}.csv.gz"


class DBIPFetcher:

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
            res = requests.get(DBIP_IP_URL, timeout=30)
            res.raise_for_status()
            return res.content
        except requests.exceptions.Timeout as e:
            raise TimeoutError(f"Request to {DBIP_IP_URL} timed out") from e
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to download from {DBIP_IP_URL}") from e
        
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
        print("Loading DB-IP data into DuckDB is not yet implemented.")
        print("CSV data size:", len(csv_bytes), "bytes")
        
objt = DBIPFetcher()
objt.fetch()