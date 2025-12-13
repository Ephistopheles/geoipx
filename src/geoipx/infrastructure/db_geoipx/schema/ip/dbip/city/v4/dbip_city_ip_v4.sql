CREATE TABLE IF NOT EXISTS dbip_city_ip_v4 (
   ip_start INET,
   ip_end INET,
   continent_code VARCHAR(4),
   country_code VARCHAR(4),
   region_code VARCHAR(4),
   city_name VARCHAR(64),
   latitude VARCHAR(24),
   longitude VARCHAR(24)
);

CREATE INDEX IF NOT EXISTS idx_dbip_city_ip_v4_ip_start_end ON dbip_city_ip_v4 (ip_start, ip_end);