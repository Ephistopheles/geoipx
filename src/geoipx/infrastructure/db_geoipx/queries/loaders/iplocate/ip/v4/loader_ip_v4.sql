WITH raw AS (
    SELECT
        network,
        continent_code,
        country_code,
        country_name,
        inet_family(network) AS family,
        inet_range_lower(network) AS ip_start,
        inet_range_upper(network) AS ip_end
    FROM read_csv_auto('{csv_path}', header=True)
)
INSERT INTO iplocate__ip_v4 (
    ip_start,
    ip_end,
    continent_code,
    country_code,
    country_name
)
SELECT
    ip_start,
    ip_end,
    continent_code,
    country_code,
    country_name
FROM raw
WHERE family = 4;
