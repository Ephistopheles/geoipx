from pathlib import Path
from datetime import datetime

class DBIPConfig:
    
    def _name_provider(self) -> str:
        return "dbip"

    def get_temp_path(self) -> Path:
        return Path.home() / ".geoipx" / "tmp" / "dbip"

    ## Config dbip country

    def _table_country_v4(self) -> str:
        return "dbip_country_ip_v4"

    def _table_country_v6(self) -> str:
        return "dbip_country_ip_v6"

    def _loader_country_v4(self) -> str:
        return "dbip_loader_country_ip_v4"

    def _loader_country_v6(self) -> str:
        return "dbip_loader_country_ip_v6"

    def _schema_country_base_path(self) -> Path:
        return Path(__file__).parents[3] / "db_geoipx" / "schema" / "ip" / "dbip" / "country"

    def _loaders_country_base_path(self) -> Path:
        return Path(__file__).parents[3] / "db_geoipx" / "queries" / "loaders" / "dbip" / "ip" / "country"

    def get_url_country(self) -> str:
        current_date = datetime.now()
        return f"https://download.db-ip.com/free/dbip-country-lite-{current_date.year}-{current_date.month}.csv.gz"

    def get_country_temp_csv_path(self) -> Path:
        return self.get_temp_path() / f"dbip_ip_country_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

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

    ## Config dbip city

    def _table_city_v4(self) -> str:
        return "dbip_city_ip_v4"

    def _table_city_v6(self) -> str:
        return "dbip_city_ip_v6"

    def _loader_city_v4(self) -> str:
        return "dbip_loader_city_ip_v4"

    def _loader_city_v6(self) -> str:
        return "dbip_loader_city_ip_v6"

    def _schema_city_base_path(self) -> Path:
        return Path(__file__).parents[3] / "db_geoipx" / "schema" / "ip" / "dbip" / "city"

    def _loaders_city_base_path(self) -> Path:
        return Path(__file__).parents[3] / "db_geoipx" / "queries" / "loaders" / "dbip" / "ip" / "city"

    def get_url_city(self) -> str:
        current_date = datetime.now()
        return f"https://download.db-ip.com/free/dbip-city-lite-{current_date.year}-{current_date.month}.csv.gz"

    def get_city_temp_csv_path(self) -> Path:
        return self.get_temp_path() / f"dbip_ip_city_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

    def sql_create_city_v4(self) -> str:
        return (self._schema_city_base_path() / "v4" / f"{self._table_city_v4()}.sql").read_text()

    def sql_create_city_v6(self) -> str:
        return (self._schema_city_base_path() / "v6" / f"{self._table_city_v6()}.sql").read_text()

    def sql_loader_city_v4(self, csv_path: Path) -> str:
        tpl = (self._loaders_city_base_path() / "v4" / f"{self._loader_city_v4()}.sql").read_text()
        return tpl.replace("{csv_path}", str(csv_path))

    def sql_loader_city_v6(self, csv_path: Path) -> str:
        tpl = (self._loaders_city_base_path() / "v6" / f"{self._loader_city_v6()}.sql").read_text()
        return tpl.replace("{csv_path}", str(csv_path))

    def sql_drop_city_v4(self) -> str:
        return f"DROP TABLE IF EXISTS {self._table_city_v4()};"

    def sql_drop_city_v6(self) -> str:
        return f"DROP TABLE IF EXISTS {self._table_city_v6()};"

    ## Config dbip asn

    def _table_asn_v4(self) -> str:
        return "dbip_asn_v4"

    def _table_asn_v6(self) -> str:
        return "dbip_asn_v6"

    def _loader_asn_v4(self) -> str:
        return "dbip_loader_asn_v4"

    def _loader_asn_v6(self) -> str:
        return "dbip_loader_asn_v6"

    def _schema_asn_base_path(self) -> Path:
        return Path(__file__).parents[3] / "db_geoipx" / "schema" / "asn" / "dbip"

    def _loaders_asn_base_path(self) -> Path:
        return Path(__file__).parents[3] / "db_geoipx" / "queries" / "loaders" / "dbip" / "asn"

    def get_url_asn(self) -> str:
        current_date = datetime.now()
        return f"https://download.db-ip.com/free/dbip-asn-lite-{current_date.year}-{current_date.month}.csv.gz"

    def get_asn_temp_csv_path(self) -> Path:
        return self.get_temp_path() / f"dbip_ip_asn_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

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
