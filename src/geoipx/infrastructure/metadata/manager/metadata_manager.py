from pathlib import Path
from geoipx.infrastructure.db_geoipx.connection.connection import GeoIPXDataBase
from geoipx.infrastructure.metadata.models.geoipx.geoipx_metadata_model import GeoIPXMetadataModel

class MetadataManager:

    def __init__(self):
        self.db = GeoIPXDataBase()

    def load_metadata(self):
       extractor_path = Path(__file__).parents[2] / "db_geoipx" / "queries" / "extractors" / "metadata" / "geoipx_metadata_extractor.sql"

       conn = self.db.conn

       try:
           result = conn.execute(extractor_path.read_text())

           return GeoIPXMetadataModel.to_model(result.fetchone()[0])
       except Exception:
           return GeoIPXMetadataModel()

    def save_metadata(self, metadata: GeoIPXMetadataModel):
        METADATA_FOLDER = Path.home() / ".geoipx" / "meta"

        METADATA_FILE = METADATA_FOLDER / "metadata.json"

        METADATA_FOLDER.mkdir(parents=True, exist_ok=True)

        METADATA_FILE.write_text(metadata.to_json(), encoding="utf-8")

        schema_path = Path(__file__).parents[2] / "db_geoipx" / "schema" / "metadata" / "geoipx_metadata.sql"
        loader_path = Path(__file__).parents[2] / "db_geoipx" / "queries" / "loaders" / "metadata" / "geoipx_metadata_loader.sql"

        conn = self.db.conn

        try:
            self.db.begin_transaction()

            conn.execute(schema_path.read_text())

            loader_sql = loader_path.read_text().replace("{{JSON_METADATA}}", metadata.to_json())
            conn.execute(loader_sql)

            self.db.commit_transaction()
        except Exception as e:
            self.db.rollback_transaction()
            raise e
