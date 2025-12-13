from datetime import datetime
from geoipx.infrastructure.providers.dbip.asn.asn_fetch import DBIPASNFetcher
from geoipx.infrastructure.metadata.manager.metadata_manager import MetadataManager
from geoipx.infrastructure.providers.iplocate.asn.asn_fetch import IPLocateASNFetcher
from geoipx.infrastructure.providers.dbip.ip.city.ip_city_fetch import DBIPCityIPFetcher
from geoipx.infrastructure.providers.ip2location.ip.v4.ip_v4_fetch import IP2LocationIPV4Fetcher
from geoipx.infrastructure.providers.ip2location.ip.v6.ip_v6_fetch import IP2LocationIPV6Fetcher
from geoipx.infrastructure.providers.dbip.ip.country.ip_country_fetch import DBIPCountryIPFetcher
from geoipx.infrastructure.providers.iplocate.ip.country.ip_country_fetch import IPLocateCountryIPFetcher
from geoipx.infrastructure.metadata.enums.geoipx_metadata_status_enums import GeoIPXMetadataStatusGlobalEnum, GeoIPXMetadataStatusProviderEnum

class GeoIPXOrchestrator:

    def check_providers_status(self):
        metadata = MetadataManager().load_metadata()
        
        if not metadata.is_initialized:
            print("Providers not initialized, first run all providers")

    def run_dbip_provider(self):
        metadata = MetadataManager().load_metadata()
        metadata_provider = metadata.providers["dbip"]

        self._process_task(metadata, metadata_provider.ip.country, DBIPCountryIPFetcher)
        self._process_task(metadata, metadata_provider.ip.city, DBIPCityIPFetcher)
        self._process_task(metadata, metadata_provider.asn, DBIPASNFetcher)

        MetadataManager().save_metadata(metadata)

    def run_ip2location_provider(self):
        metadata = MetadataManager().load_metadata()
        metadata_provider = metadata.providers["ip2location"]

        self._process_task(metadata, metadata_provider.ip.v4, IP2LocationIPV4Fetcher)
        self._process_task(metadata, metadata_provider.ip.v6, IP2LocationIPV6Fetcher)

        MetadataManager().save_metadata(metadata)

    def run_iplocate_provider(self):
        metadata = MetadataManager().load_metadata()
        metadata_provider = metadata.providers["iplocate"]

        self._process_task(metadata, metadata_provider.ip.country, IPLocateCountryIPFetcher)
        self._process_task(metadata, metadata_provider.asn, IPLocateASNFetcher)

        MetadataManager().save_metadata(metadata)

    def _process_task(self, metadata, task_node, fetcher_cls):
        should_run = False
        
        if task_node.status in [GeoIPXMetadataStatusProviderEnum.NEVER_RUN, GeoIPXMetadataStatusProviderEnum.FAILED]:
            should_run = True
        elif task_node.status == GeoIPXMetadataStatusProviderEnum.SUCCESS:
            last_update = task_node.last_update
            if last_update:
                if last_update.month != datetime.now().month:
                    should_run = True
            else:
                should_run = True

        if should_run:
            result = fetcher_cls().fetch()

            task_node.last_update = datetime.now()
            
            if result.success:
                metadata.global_status = GeoIPXMetadataStatusGlobalEnum.PARTIAL_SUCCESS
                task_node.status = GeoIPXMetadataStatusProviderEnum.SUCCESS
                task_node.records_count = result.records_count
                task_node.last_error = None
            else:
                task_node.status = GeoIPXMetadataStatusProviderEnum.FAILED
                task_node.last_error = result.error_message or "An unknown error occurred"

# pruebas locales
if __name__ == "__main__":
    orchestrator = GeoIPXOrchestrator()
    orchestrator.run_dbip_provider()
    orchestrator.run_ip2location_provider()
    orchestrator.run_iplocate_provider()

