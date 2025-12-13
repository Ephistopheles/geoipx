import io
import zipfile
import requests
from geoipx.infrastructure.db_geoipx.connection.database_connection import GeoIPXDataBase
from geoipx.infrastructure.providers.result_model.provider_fetch_result import ProviderFetchResult
from geoipx.infrastructure.providers.ip2location.config_provider.config_ip2location import IP2LocationConfig

class IP2LocationIPV6Fetcher:

    def __init__(self):
        self.config = IP2LocationConfig()

    def fetch(self) -> ProviderFetchResult:
        try:
            compressed = self._download()
            decompressed = self._descompress(compressed)
            records_count = self._load_into_duckdb(decompressed)

            return ProviderFetchResult(success=True, error_message=None, records_count=records_count)
        except Exception as e:
            return ProviderFetchResult(success=False, error_message=str(e), records_count=None)
    
    def _download(self) -> bytes:
        try:
            # pruebas locales
            # res = requests.get(self.config.get_url_ip_v6(), timeout=30)
            # res.raise_for_status()
            # return res.content

            with open("/home/memphis/Proyects/workspace-back/geoipx/IP2LOCATION-LITE-DB11.IPV6.CSV.zip", "rb") as f:
                return f.read()

        except requests.exceptions.Timeout as e:
            raise TimeoutError(f"Request to {self.config.get_url_ip_v6()} timed out") from e
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to download from {self.config.get_url_ip_v6()}") from e
        
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

    def _load_into_duckdb(self, csv_bytes: bytes) -> int:
        cfg = self.config

        cfg.get_temp_path().mkdir(parents=True, exist_ok=True)

        tmp_csv_path = cfg.get_ip_v6_temp_csv_path()
        tmp_csv_path.write_bytes(csv_bytes)

        db = GeoIPXDataBase()
        conn = db.conn

        try:
            db.begin_transaction()

            conn.execute(cfg.sql_drop_table_ip_v6())

            conn.execute(cfg.sql_create_table_ip_v6())

            conn.execute(cfg.sql_loader_ip_v6(tmp_csv_path))

            db.commit_transaction()

            return conn.execute(cfg.sql_count_ip_v6()).fetchone()[0]
        except Exception as e:
            db.rollback_transaction()
            raise e
        finally:
            tmp_csv_path.unlink()
