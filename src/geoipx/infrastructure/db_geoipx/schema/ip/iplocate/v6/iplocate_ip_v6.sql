CREATE TABLE IF NOT EXISTS iplocate__ip_v6 (
    ip_start HUGEINT,
    ip_end HUGEINT,
    continent_code VARCHAR(4),
    country_code VARCHAR(4),
    country_name VARCHAR(64)
);