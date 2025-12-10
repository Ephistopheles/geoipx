WITH raw AS (
    SELECT
        col0::INET AS ip_start,
        col1::INET AS ip_end,
        col2 AS asn,
        col3 AS name
    FROM read_csv('{csv_path}',
        header = false,
        quote = '"',
        auto_detect = false,
        strict_mode = false,
        columns = {
            'col0': 'VARCHAR',
            'col1': 'VARCHAR',
            'col2': 'VARCHAR',
            'col3': 'VARCHAR'
        }
    )
)
INSERT INTO dbip_asn_v6 (
    ip_start,
    ip_end,
    asn,
    name
)
SELECT
    ip_start,
    ip_end,
    asn,
    name
FROM raw
WHERE family(ip_start) = 6;
