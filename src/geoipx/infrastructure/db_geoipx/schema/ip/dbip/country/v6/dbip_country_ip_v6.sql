CREATE TABLE IF NOT EXISTS dbip_country_ip_v6 (
   ip_start INET,
   ip_end INET,
   country_code VARCHAR(4)
);

CREATE INDEX IF NOT EXISTS idx_dbip_country_ip_v6_ip_start_end ON dbip_country_ip_v6 (ip_start, ip_end);