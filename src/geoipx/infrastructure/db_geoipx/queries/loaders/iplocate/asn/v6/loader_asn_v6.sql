WITH raw AS (
    SELECT
        network::INET AS network,
        asn,
        country_code,
        name,
        org,
        domain
    FROM read_csv('{csv_path}',
        header = true,
        quote = '"',
        auto_detect = false,
        strict_mode = false,
        columns = {
            'network': 'VARCHAR',
            'asn': 'VARCHAR',
            'country_code': 'VARCHAR',
            'name': 'VARCHAR',
            'org': 'VARCHAR',
            'domain': 'VARCHAR'
        }
    )
)
INSERT INTO iplocate__asn_v6 (
    network,
    asn,
    country_code,
    name,
    org,
    domain
)
SELECT
    network,
    asn,
    country_code,
    name,
    org,
    domain
FROM raw
WHERE family(network) = 6;
