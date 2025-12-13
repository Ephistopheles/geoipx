CREATE TABLE IF NOT EXISTS iplocate_asn_v6 (
    network INET,
    asn VARCHAR(20),
    country_code VARCHAR(3),
    name VARCHAR(64),
    org VARCHAR(64),
    domain VARCHAR(64)
);

CREATE INDEX IF NOT EXISTS idx_iplocate_asn_v6_network ON iplocate_asn_v6 (network);
