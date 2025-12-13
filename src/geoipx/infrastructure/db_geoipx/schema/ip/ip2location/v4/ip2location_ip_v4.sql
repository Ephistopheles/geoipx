CREATE TABLE IF NOT EXISTS ip2location_ip_v4 (
    ip_start VARCHAR(39),
    ip_end VARCHAR(39),
    country_code VARCHAR(2),
    country_name VARCHAR(64),
    region_name VARCHAR(64),
    city_name VARCHAR(64),
    latitude VARCHAR(24),
    longitude VARCHAR(24),
    zip_code VARCHAR(64),
    timezone VARCHAR(64)
);

CREATE INDEX IF NOT EXISTS idx_ip2location_ip_v4_ip_start_end ON ip2location_ip_v4 (ip_start, ip_end);