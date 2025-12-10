WITH raw AS (
    SELECT
        col0::INET AS ip_start,
        col1::INET AS ip_end,
        col2       AS country_code
    FROM read_csv('{csv_path}',
        header = false,
        quote = '"',
        auto_detect = false,
        strict_mode = false,
        columns = {
            'col0': 'VARCHAR',
            'col1': 'VARCHAR',
            'col2': 'VARCHAR'
        }
    )
)
INSERT INTO dbip_country_ip_v6 (
    ip_start,
    ip_end,
    country_code
)
SELECT
    ip_start,
    ip_end,
    country_code
FROM raw
WHERE family(ip_start) = 6;
