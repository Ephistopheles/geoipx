import io
import zipfile
import requests
from pathlib import Path
from geoipx.infrastructure.db_geoipx.connection.connection import GeoIPXDataBase
from geoipx.infrastructure.providers.iplocate.config_provider.config_iplocate import IPLocateConfig

class IPLocateASNFetcher:
    
    def __init__(self):
        self.config = IPLocateConfig()
    
    def fetch(self):
        try:
            compressed = self._download()
            decompressed = self._descompress(compressed)
            self._load_into_duckdb(decompressed)
        except Exception as e:
            raise RuntimeError("Failed to fetch and process data") from e
    
    def _download(self) -> bytes:
        try:
            res = requests.get(self.config.get_url_asn(), timeout=30)
            res.raise_for_status()
            return res.content
        except requests.exceptions.Timeout as e:
            raise TimeoutError(f"Request to {self.config.get_url_asn()} timed out") from e
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to download from {self.config.get_url_asn()}") from e
        
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
        cfg = self.config

        cfg.get_temp_path().mkdir(parents=True, exist_ok=True)

        tmp_csv_path = cfg.get_asn_temp_csv_path()
        tmp_csv_path.write_bytes(csv_bytes)

        db = GeoIPXDataBase()
        conn = db.conn

        try:
            db.begin_transaction()

            conn.execute(cfg.sql_drop_asn_v4())
            conn.execute(cfg.sql_drop_asn_v6())

            conn.execute(cfg.sql_create_asn_v4())
            conn.execute(cfg.sql_create_asn_v6())

            conn.execute(cfg.sql_loader_asn_v4(tmp_csv_path))
            conn.execute(cfg.sql_loader_asn_v6(tmp_csv_path))

            db.commit_transaction()
        except Exception as e:
            db.rollback_transaction()
            raise
        finally:
            tmp_csv_path.unlink()
