from pathlib import Path
from datetime import datetime

class IP2LocationConfig:
    
    def _name_provider(self) -> str:
        return "ip2location"

    def get_temp_path(self) -> Path:
      return Path.home() / ".geoipx" / "tmp" / "ip2location"

    ## Config ip2location ipv4

    def _table_ip_v4(self) -> str:
      return "ip2location_ip_v4"

    def _loader_ip_v4(self) -> str:
      return "ip2location_loader_ip_v4"

    def _schema_ip_v4_base_path(self) -> Path:
      return Path(__file__).parents[3] / "db_geoipx" / "schema" / "ip" / "ip2location"

    def _loader_ip_v4_base_path(self) -> Path:
      return Path(__file__).parents[3] / "db_geoipx" / "queries" / "loaders" / "ip2location" / "ip"

    def get_url_ip_v4(self) -> str:
        TOKEN_IP2LOCATION = "LbLuGQmzPOLDBiQ4RpY2bb5kAam7oI8pcU0JyoWfa3qhtu4XItCRIahrLwgERYx4"
        DATABASE_CODE_IP2LOCATION = "DB11LITECSV"
        return f"https://www.ip2location.com/download/?token={TOKEN_IP2LOCATION}&file={DATABASE_CODE_IP2LOCATION}"

    def get_ip_v4_temp_csv_path(self) -> Path:
      return self.get_temp_path() / f"ip2location_ip_v4_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

    def sql_create_table_ip_v4(self) -> str:
      return (self._schema_ip_v4_base_path() / "v4" / f"{self._table_ip_v4()}.sql").read_text()

    def sql_loader_ip_v4(self, csv_path: Path) -> str:
      tpl = (self._loader_ip_v4_base_path() / "v4" / f"{self._loader_ip_v4()}.sql").read_text()
      return tpl.replace("{csv_path}", str(csv_path))

    def sql_count_ip_v4(self) -> str:
      return f"SELECT COUNT(*) FROM {self._table_ip_v4()};"

    def sql_drop_table_ip_v4(self) -> str:
      return f"DROP TABLE IF EXISTS {self._table_ip_v4()};"

    ## Config ip2location ipv6

    def _table_ip_v6(self) -> str:
      return "ip2location_ip_v6"

    def _loader_ip_v6(self) -> str:
      return "ip2location_loader_ip_v6"

    def _schema_ip_v6_base_path(self) -> Path:
      return Path(__file__).parents[3] / "db_geoipx" / "schema" / "ip" / "ip2location"

    def _loader_ip_v6_base_path(self) -> Path:
      return Path(__file__).parents[3] / "db_geoipx" / "queries" / "loaders" / "ip2location" / "ip"

    def get_url_ip_v6(self) -> str:
        TOKEN_IP2LOCATION = "LbLuGQmzPOLDBiQ4RpY2bb5kAam7oI8pcU0JyoWfa3qhtu4XItCRIahrLwgERYx4"
        DATABASE_CODE_IP2LOCATION = "DB11LITECSVIPV6"
        return f"https://www.ip2location.com/download/?token={TOKEN_IP2LOCATION}&file={DATABASE_CODE_IP2LOCATION}"

    def get_ip_v6_temp_csv_path(self) -> Path:
      return self.get_temp_path() / f"ip2location_ip_v6_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

    def sql_create_table_ip_v6(self) -> str:
      return (self._schema_ip_v6_base_path() / "v6" / f"{self._table_ip_v6()}.sql").read_text()

    def sql_loader_ip_v6(self, csv_path: Path) -> str:
      tpl = (self._loader_ip_v6_base_path() / "v6" / f"{self._loader_ip_v6()}.sql").read_text()
      return tpl.replace("{csv_path}", str(csv_path))

    def sql_count_ip_v6(self) -> str:
      return f"SELECT COUNT(*) FROM {self._table_ip_v6()};"

    def sql_drop_table_ip_v6(self) -> str:
      return f"DROP TABLE IF EXISTS {self._table_ip_v6()};"
