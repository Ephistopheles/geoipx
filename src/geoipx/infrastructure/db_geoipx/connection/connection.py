import duckdb
from pathlib import Path

class GeoIPXDataBase:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
           cls._instance = super().__new__(cls)
           
           cls._db_path = Path.home() / ".geoipx" / "geoipx.duckdb"
           cls._db_path.parent.mkdir(parents=True, exist_ok=True)
           
           cls._connection = duckdb.connect(database=str(cls._db_path), read_only=False)
           
        return cls._instance
    
    @property
    def conn(self):
        """Get the DuckDB connection instance."""
        return self._connection
    
    def close(self):
        """Close the DuckDB connection."""
        if self._connection:
            self._connection.close()
            self._connection = None
            GeoIPXDataBase._instance = None