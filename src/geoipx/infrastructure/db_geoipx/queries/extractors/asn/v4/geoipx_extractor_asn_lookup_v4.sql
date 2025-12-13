WITH input_ip AS (
    SELECT {{IP}}::INET AS addr
)
SELECT * FROM (
    SELECT
        'dbip' AS provider,
        CAST(dav.ip_start AS VARCHAR) || ' - ' || CAST(dav.ip_end AS VARCHAR) AS resolved_range,
        dav.asn,
        dav.name,
        NULL AS org,
        NULL AS domain,
        NULL AS country_code
    FROM dbip_asn_v4 AS dav, input_ip
    WHERE input_ip.addr >= dav.ip_start
      AND input_ip.addr <= dav.ip_end
    UNION ALL
    SELECT
        'iplocate' AS provider,
        CAST(iav.network AS VARCHAR) AS resolved_range,
        iav.asn,
        iav.name,
        iav.org,
        iav.domain,
        iav.country_code
    FROM iplocate_asn_v4 AS iav, input_ip
    WHERE input_ip.addr <<= iav.network
);
