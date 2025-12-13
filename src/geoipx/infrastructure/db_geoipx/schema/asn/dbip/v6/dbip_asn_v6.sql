CREATE TABLE IF NOT EXISTS dbip_asn_v6 (
    ip_start INET,
    ip_end INET,
    asn VARCHAR(20),
    name VARCHAR(64)
);

CREATE INDEX IF NOT EXISTS idx_dbip_asn_v6_ip_start_end ON dbip_asn_v6 (ip_start, ip_end);