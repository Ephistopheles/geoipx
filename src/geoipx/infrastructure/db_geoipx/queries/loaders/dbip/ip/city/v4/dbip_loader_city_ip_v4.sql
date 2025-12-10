WITH raw AS (
    SELECT
        col0::INET AS ip_start,
        col1::INET AS ip_end,
        col2 AS continent_code,
        col3 AS country_code,
        col4 AS region_code,
        col5 AS city_name,
        NULLIF(col6, '')::DOUBLE AS latitude,
        NULLIF(col7, '')::DOUBLE AS longitude
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
            'col7': 'VARCHAR'
        }
    )
)
INSERT INTO dbip__city__ip_v4 (
    ip_start,
    ip_end,
    continent_code,
    country_code,
    region_code,
    city_name,
    latitude,
    longitude
)
SELECT
    ip_start,
    ip_end,
    continent_code,
    country_code,
    region_code,
    city_name,
    latitude,
    longitude
FROM raw
WHERE family(ip_start) = 4;
