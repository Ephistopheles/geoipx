import io
import zipfile
import requests
from geoipx.infrastructure.db_geoipx.connection.database_connection import GeoIPXDataBase
from geoipx.infrastructure.providers.result_model.provider_fetch_result import ProviderFetchResult
from geoipx.infrastructure.providers.iplocate.config_provider.config_iplocate import IPLocateConfig

class IPLocateCountryIPFetcher:

    def __init__(self):
        self.config = IPLocateConfig()
    
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
            res = requests.get(self.config.get_url_country(), timeout=30)
            res.raise_for_status()
            return res.content
        except requests.exceptions.Timeout as e:
            raise TimeoutError(f"Request to {self.config.get_url_country()} timed out") from e
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to download from {self.config.get_url_country()}") from e
        
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

    def _load_into_duckdb(self, csv_bytes: bytes) -> int:
        cfg = self.config
        
        cfg.get_temp_path().mkdir(parents=True, exist_ok=True)

        tmp_csv_path = cfg.get_country_temp_csv_path()
        tmp_csv_path.write_bytes(csv_bytes)

        db = GeoIPXDataBase()
        conn = db.conn

        try:
            db.begin_transaction()

            conn.execute(cfg.sql_drop_country_v4())
            conn.execute(cfg.sql_drop_country_v6())

            conn.execute(cfg.sql_create_country_v4())
            conn.execute(cfg.sql_create_country_v6())

            conn.execute(cfg.sql_loader_country_v4(tmp_csv_path))
            conn.execute(cfg.sql_loader_country_v6(tmp_csv_path))

            db.commit_transaction()

            country_v4_count = conn.execute(cfg.sql_count_country_v4()).fetchone()[0]
            country_v6_count = conn.execute(cfg.sql_count_country_v6()).fetchone()[0]
            
            return country_v4_count + country_v6_count
        except Exception as e:
            db.rollback_transaction()
            raise e
        finally:
            tmp_csv_path.unlink(missing_ok=True)
