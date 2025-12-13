import io
import gzip
import requests
from geoipx.infrastructure.db_geoipx.connection.connection import GeoIPXDataBase
from geoipx.infrastructure.providers.dbip.config_provider.config_dbip import DBIPConfig
from geoipx.infrastructure.providers.result_model.ProviderFetchResult import ProviderFetchResult

class DBIPCityIPFetcher:

    def __init__(self):
        self.config = DBIPConfig()
    
    def fetch(self) -> ProviderFetchResult:
        try:
            compressed = self._download()
            decompressed = self._descompress(compressed)
            records_count = self._load_into_duckdb(decompressed)

            return ProviderFetchResult(success=True, error_message=None, records_count=records_count)
        except Exception as e:
            raise RuntimeError("Failed to fetch and process data") from e
    
    def _download(self) -> bytes:
        try:
            res = requests.get(self.config.get_url_city(), timeout=30)
            res.raise_for_status()
            return res.content
        except requests.exceptions.Timeout as e:
            raise TimeoutError(f"Request to {self.config.get_url_city()} timed out") from e
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to download from {self.config.get_url_city()}") from e
        
    def _descompress(self, data: bytes) -> bytes:
        try:
            with gzip.GzipFile(fileobj=io.BytesIO(data)) as gz_file:
                file = gz_file.read()
                if not file:
                    raise ValueError("GZ file is empty")
                return file
        except OSError as e:
            raise ValueError("Invalid GZ file") from e
        
    def _load_into_duckdb(self, csv_bytes: bytes) -> int:
        cfg = self.config

        cfg.get_temp_path().mkdir(parents=True, exist_ok=True)

        tmp_csv_path = cfg.get_city_temp_csv_path()
        tmp_csv_path.write_bytes(csv_bytes)
        
        db = GeoIPXDataBase()
        conn = db.conn

        try:
            db.begin_transaction()

            conn.execute(cfg.sql_drop_city_v4())
            conn.execute(cfg.sql_drop_city_v6())

            conn.execute(cfg.sql_create_city_v4())
            conn.execute(cfg.sql_create_city_v6())

            conn.execute(cfg.sql_loader_city_v4(tmp_csv_path))
            conn.execute(cfg.sql_loader_city_v6(tmp_csv_path))

            db.commit_transaction()

            city_v4_count = conn.execute(cfg.sql_count_city_v4()).fetchone()[0]
            city_v6_count = conn.execute(cfg.sql_count_city_v6()).fetchone()[0]
            
            return city_v4_count + city_v6_count
        except Exception as e:
            db.rollback_transaction()
            raise e
        finally:
            tmp_csv_path.unlink(missing_ok=True)
