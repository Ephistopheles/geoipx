WITH raw AS (
    SELECT
        col0 AS ip_start,
        col1 AS ip_end,
        col2 AS country_code,
        col3 AS country_name,
        col4 AS region_name,
        col5 AS city_name,
        col6 AS latitude,
        col7 AS longitude,
        col8 AS zip_code,
        col9 AS timezone
    FROM read_csv('{csv_path}',
        header = false,
        quote = '"',
        auto_detect = false,
        strict_mode = false,
        columns = {
            'col0': 'VARCHAR',
            'col1': 'VARCHAR',
            'col2': 'VARCHAR',
            'col3': 'VARCHAR',
            'col4': 'VARCHAR',
            'col5': 'VARCHAR',
            'col6': 'VARCHAR',
            'col7': 'VARCHAR',
            'col8': 'VARCHAR',
            'col9': 'VARCHAR'
        }
    )
)
INSERT INTO ip2location_ip_v6 (
    ip_start,
    ip_end,
    country_code,
    country_name,
    region_name,
    city_name,
    latitude,
    longitude,
    zip_code,
    timezone
)
SELECT
    ip_start,
    ip_end,
    country_code,
    country_name,
    region_name,
    city_name,
    latitude,
    longitude,
    zip_code,
    timezone
FROM raw;
