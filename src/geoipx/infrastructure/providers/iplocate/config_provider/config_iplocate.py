from pathlib import Path
from datetime import datetime

class IPLocateConfig:

   def _name_provider(self) -> str:
      return "iplocate"

   def get_temp_path(self) -> Path:
      return Path.home() / ".geoipx" / "tmp" / "iplocate"

   ## Config iplocate country

   def _table_country_v4(self) -> str:
      return "iplocate_country_ip_v4"

   def _table_country_v6(self) -> str:
      return "iplocate_country_ip_v6"

   def _loader_country_v4(self) -> str:
      return "iplocate_loader_country_ip_v4"

   def _loader_country_v6(self) -> str:
      return "iplocate_loader_country_ip_v6"

   def _schema_country_base_path(self) -> Path:
      return Path(__file__).parents[3] / "db_geoipx" / "schema" / "ip" / "iplocate" / "country"

   def _loaders_country_base_path(self) -> Path:
      return Path(__file__).parents[3] / "db_geoipx" / "queries" / "loaders" / "iplocate" / "ip" / "country"

   def get_url_country(self) -> str:
      return "https://github.com/iplocate/ip-address-databases/raw/refs/heads/main/ip-to-country/ip-to-country.csv.zip"

   def get_country_temp_csv_path(self) -> Path:
      return self.get_temp_path() / f"iplocate_ip_country_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

   def sql_create_country_v4(self) -> str:
      return (self._schema_country_base_path() / "v4" / f"{self._table_country_v4()}.sql").read_text()

   def sql_create_country_v6(self) -> str:
      return (self._schema_country_base_path() / "v6" / f"{self._table_country_v6()}.sql").read_text()
      
   def sql_loader_country_v4(self, csv_path: Path) -> str:
      tpl = (self._loaders_country_base_path() / "v4" / f"{self._loader_country_v4()}.sql").read_text()
      return tpl.replace("{csv_path}", str(csv_path))

   def sql_loader_country_v6(self, csv_path: Path) -> str:
      tpl = (self._loaders_country_base_path() / "v6" / f"{self._loader_country_v6()}.sql").read_text()
      return tpl.replace("{csv_path}", str(csv_path))
    
   def sql_drop_country_v4(self) -> str:
      return f"DROP TABLE IF EXISTS {self._table_country_v4()};"

   def sql_drop_country_v6(self) -> str:
      return f"DROP TABLE IF EXISTS {self._table_country_v6()};"

   ## Config iplocate asn

   def _table_asn_v4(self) -> str:
      return "iplocate_asn_v4"

   def _table_asn_v6(self) -> str:
      return "iplocate_asn_v6"

   def _loader_asn_v4(self) -> str:
      return "iplocate_loader_asn_v4"

   def _loader_asn_v6(self) -> str:
      return "iplocate_loader_asn_v6"   

   def _schema_asn_base_path(self) -> Path:
      return Path(__file__).parents[3] / "db_geoipx" / "schema" / "asn" / "iplocate"

   def _loaders_asn_base_path(self) -> Path:
      return Path(__file__).parents[3] / "db_geoipx" / "queries" / "loaders" / "iplocate" / "asn"

   def get_url_asn(self) -> str:
      return "https://github.com/iplocate/ip-address-databases/raw/refs/heads/main/ip-to-asn/ip-to-asn.csv.zip"

   def get_asn_temp_csv_path(self) -> Path:
      return self.get_temp_path() / f"iplocate_asn_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

   def sql_create_asn_v4(self) -> str:
      return (self._schema_asn_base_path() / "v4" / f"{self._table_asn_v4()}.sql").read_text()

   def sql_create_asn_v6(self) -> str:
      return (self._schema_asn_base_path() / "v6" / f"{self._table_asn_v6()}.sql").read_text()
      
   def sql_loader_asn_v4(self, csv_path: Path) -> str:
      tpl = (self._loaders_asn_base_path() / "v4" / f"{self._loader_asn_v4()}.sql").read_text()
      return tpl.replace("{csv_path}", str(csv_path))

   def sql_loader_asn_v6(self, csv_path: Path) -> str:
      tpl = (self._loaders_asn_base_path() / "v6" / f"{self._loader_asn_v6()}.sql").read_text()
      return tpl.replace("{csv_path}", str(csv_path))

   def sql_drop_asn_v4(self) -> str:
      return f"DROP TABLE IF EXISTS {self._table_asn_v4()};"

   def sql_drop_asn_v6(self) -> str:
      return f"DROP TABLE IF EXISTS {self._table_asn_v6()};"
