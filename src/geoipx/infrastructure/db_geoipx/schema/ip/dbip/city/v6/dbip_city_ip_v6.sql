CREATE TABLE IF NOT EXISTS dbip__city__ip_v6 (
  ip_start INET,
   ip_end INET,
   continent_code VARCHAR(4),
   country_code VARCHAR(4),
   region_code VARCHAR(4),
   city_name VARCHAR(64),
   latitude VARCHAR(24),
   longitude VARCHAR(24)
);