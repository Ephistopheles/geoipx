CREATE TABLE IF NOT EXISTS iplocate__ip_v4 (
   ip_start BIGINT,
   ip_end BIGINT,
   continent_code VARCHAR(4),
   country_code VARCHAR(4),
   country_name VARCHAR(64)
);