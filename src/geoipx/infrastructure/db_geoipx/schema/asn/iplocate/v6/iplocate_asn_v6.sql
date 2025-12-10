CREATE TABLE IF NOT EXISTS iplocate__asn_v6 (
    network INET,
    asn VARCHAR(20),
    country_code VARCHAR(3),
    name VARCHAR(64),
    org VARCHAR(64),
    domain VARCHAR(64)
);