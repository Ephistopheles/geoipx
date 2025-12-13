import threading
from datetime import datetime, timedelta
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

    def run_orchestrator(self):
        metadata = MetadataManager().load_metadata()
        
        is_first_run = (
            not metadata.is_initialized or
            metadata.global_status == GeoIPXMetadataStatusGlobalEnum.NEVER_RUN
        )

        if is_first_run:
            self._run_all_providers()
            # TODO: Loader type spiner or apt
            self._finalize_run()
        else:
            self._run_background_update()

    def _run_background_update(self):
        def _background_update_job():
            try:
                self._run_all_providers()
                self._finalize_run()
            except Exception:
                pass

        thread = threading.Thread(
            target=_background_update_job,
            daemon=True
        )
        thread.start()

    def _run_all_providers(self):
        self._run_dbip_provider()
        self._run_ip2location_provider()
        self._run_iplocate_provider()

    def _finalize_run(self):
        metadata_manager = MetadataManager()
        metadata = metadata_manager.load_metadata()

        metadata.last_global_update = datetime.now()
        metadata.is_initialized = True

        provider_states = [
            p.status
            for provider in metadata.providers.values()
            for p in provider.iter_tasks()
        ]

        if provider_states and all(s == GeoIPXMetadataStatusProviderEnum.SUCCESS for s in provider_states):
            metadata.global_status = GeoIPXMetadataStatusGlobalEnum.SUCCESS
        elif any(s == GeoIPXMetadataStatusProviderEnum.SUCCESS for s in provider_states):
            metadata.global_status = GeoIPXMetadataStatusGlobalEnum.PARTIAL_SUCCESS
        else:
            metadata.global_status = GeoIPXMetadataStatusGlobalEnum.FAILED


        metadata_manager.save_metadata(metadata)

    def _run_dbip_provider(self):
        metadata = MetadataManager().load_metadata()
        metadata_provider = metadata.providers["dbip"]

        def _process_dbip_task(metadata, task_node, fetcher_cls):
            should_run = False
            
            if task_node.status in [GeoIPXMetadataStatusProviderEnum.NEVER_RUN, GeoIPXMetadataStatusProviderEnum.FAILED]:
                should_run = True
            elif task_node.status == GeoIPXMetadataStatusProviderEnum.SUCCESS:
                last_update = task_node.last_update
                if last_update and last_update.month != datetime.now().month:
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

        _process_dbip_task(metadata, metadata_provider.ip.country, DBIPCountryIPFetcher)
        _process_dbip_task(metadata, metadata_provider.ip.city, DBIPCityIPFetcher)
        _process_dbip_task(metadata, metadata_provider.asn, DBIPASNFetcher)

        MetadataManager().save_metadata(metadata)

    def _run_ip2location_provider(self):
        metadata = MetadataManager().load_metadata()
        metadata_provider = metadata.providers["ip2location"]

        def _process_ip2location_task(metadata, task_node, fetcher_cls):
            should_run = False
            now = datetime.now()

            if task_node.rate_limit_remaining is None:
                task_node.rate_limit_remaining = 5

            if task_node.rate_limit_remaining == 0:
                if task_node.rate_limit_reset_at and now < task_node.rate_limit_reset_at:
                    task_node.status = GeoIPXMetadataStatusProviderEnum.RATE_LIMITED
                    return
                else:
                    task_node.rate_limit_remaining = 5
                    task_node.rate_limit_reset_at = None
                    task_node.status = GeoIPXMetadataStatusProviderEnum.FAILED

            if task_node.status in [GeoIPXMetadataStatusProviderEnum.NEVER_RUN, GeoIPXMetadataStatusProviderEnum.FAILED]:
                should_run = True
            elif task_node.status == GeoIPXMetadataStatusProviderEnum.SUCCESS:
                last_update = task_node.last_update
                if not last_update or last_update.month != now.month:
                    should_run = True

            if should_run:
                result = fetcher_cls().fetch()

                task_node.last_update = now
                task_node.rate_limit_remaining -= 1

                if task_node.rate_limit_remaining == 0 and task_node.rate_limit_reset_at is None:
                    task_node.rate_limit_reset_at = now + timedelta(hours=24)

                if result.success:
                    metadata.global_status = GeoIPXMetadataStatusGlobalEnum.PARTIAL_SUCCESS
                    task_node.status = GeoIPXMetadataStatusProviderEnum.SUCCESS
                    task_node.records_count = result.records_count
                    task_node.last_error = None
                else:
                    task_node.status = GeoIPXMetadataStatusProviderEnum.FAILED
                    task_node.last_error = result.error_message or "An unknown error occurred"

        _process_ip2location_task(metadata, metadata_provider.ip.v4, IP2LocationIPV4Fetcher)
        _process_ip2location_task(metadata, metadata_provider.ip.v6, IP2LocationIPV6Fetcher)

        MetadataManager().save_metadata(metadata)

    def _run_iplocate_provider(self):
        metadata = MetadataManager().load_metadata()
        metadata_provider = metadata.providers["iplocate"]

        def _process_iplocate_task(metadata, task_node, fetcher_cls):
            should_run = False
            
            if task_node.status in [GeoIPXMetadataStatusProviderEnum.NEVER_RUN, GeoIPXMetadataStatusProviderEnum.FAILED]:
                should_run = True
            elif task_node.status == GeoIPXMetadataStatusProviderEnum.SUCCESS:
                last_update = task_node.last_update
                if last_update and last_update.month != datetime.now().month:
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

        _process_iplocate_task(metadata, metadata_provider.ip.country, IPLocateCountryIPFetcher)
        _process_iplocate_task(metadata, metadata_provider.asn, IPLocateASNFetcher)

        MetadataManager().save_metadata(metadata)
