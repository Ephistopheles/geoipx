CREATE TABLE IF NOT EXISTS iplocate_country_ip_v6 (
    network INET,
    continent_code VARCHAR(4),
    country_code VARCHAR(4),
    country_name VARCHAR(64)
);

CREATE INDEX IF NOT EXISTS idx_iplocate_country_ip_v6_network ON iplocate_country_ip_v6 (network);