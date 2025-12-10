WITH raw AS (
    SELECT
        network::INET AS network,
        continent_code,
        country_code,
        country_name
    FROM read_csv('{csv_path}',
        header = true,
        quote = '"',
        auto_detect = false,
        strict_mode = false,
        columns = {
            'network': 'VARCHAR',
            'continent_code': 'VARCHAR',
            'country_code': 'VARCHAR',
            'country_name': 'VARCHAR'
        }
    )
)
INSERT INTO iplocate__country__ip_v6 (
    network,
    continent_code,
    country_code,
    country_name
)
SELECT
    network,
    continent_code,
    country_code,
    country_name
FROM raw
WHERE family(network) = 6;
