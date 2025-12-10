from pathlib import Path
from datetime import datetime

class IPLocateConfig:

   def _name_provider(self) -> str:
      return "iplocate"

   def _table_v4(self) -> str:
      return "iplocate_country_ip_v4"

   def _table_v6(self) -> str:
      return "iplocate_country_ip_v6"

   def _loader_v4(self) -> str:
      return "iplocate_loader_country_ip_v4"

   def _loader_v6(self) -> str:
      return "iplocate_loader_country_ip_v6"

   def _schema_base_path(self) -> Path:
      return Path(__file__).parents[3] / "db_geoipx" / "schema" / "ip" / "iplocate" / "country"

   def _loaders_base_path(self) -> Path:
      return Path(__file__).parents[3] / "db_geoipx" / "queries" / "loaders" / "iplocate" / "ip" / "country"

   def get_temp_path(self) -> Path:
      return Path.home() / ".geoipx" / "tmp" / "iplocate"

   def get_temp_csv_path(self) -> Path:
      return self.get_temp_path() / f"iplocate_ip_country_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

   def sql_create_v4(self) -> str:
      return (self._schema_base_path() / "v4" / f"{self._table_v4()}.sql").read_text()

   def sql_create_v6(self) -> str:
      return (self._schema_base_path() / "v6" / f"{self._table_v6()}.sql").read_text()
      
   def sql_loader_v4(self, csv_path: Path) -> str:
      tpl = (self._loaders_base_path() / "v4" / f"{self._loader_v4()}.sql").read_text()
      return tpl.replace("{csv_path}", str(csv_path))

   def sql_loader_v6(self, csv_path: Path) -> str:
      tpl = (self._loaders_base_path() / "v6" / f"{self._loader_v6()}.sql").read_text()
      return tpl.replace("{csv_path}", str(csv_path))
    
   def sql_drop_v4(self) -> str:
      return f"DROP TABLE IF EXISTS {self._table_v4()};"

   def sql_drop_v6(self) -> str:
      return f"DROP TABLE IF EXISTS {self._table_v6()};"
