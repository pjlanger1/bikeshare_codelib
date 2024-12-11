CREATE TABLE rawbikes_aggregated AS
SELECT 
    b.stationid,
    b.monthidx,
    b.weekday,
    b.shift,
    COUNT(*) AS total_records,
    AVG((CAST(b.num_bikes_available AS DOUBLE) - CAST(b.num_ebikes_available AS DOUBLE)) / CAST(COALESCE(b.capacity, 1) AS DOUBLE)) AS avg_perc_acoustic,
    VAR_POP((CAST(b.num_bikes_available AS DOUBLE) - CAST(b.num_ebikes_available AS DOUBLE)) / CAST(COALESCE(b.capacity, 1) AS DOUBLE)) AS var_perc_acoustic,
    AVG(CAST(b.num_ebikes_available AS DOUBLE) / CAST(COALESCE(b.capacity, 1) AS DOUBLE)) AS avg_perc_electric,
    VAR_POP(CAST(b.num_ebikes_available AS DOUBLE) / CAST(COALESCE(b.capacity, 1) AS DOUBLE)) AS var_perc_electric,
    AVG(CAST(b.num_docks_disabled AS DOUBLE) / CAST(COALESCE(b.capacity, 1) AS DOUBLE)) AS avg_perc_bad_docks,
    VAR_POP(CAST(b.num_docks_disabled AS DOUBLE) / CAST(COALESCE(b.capacity, 1) AS DOUBLE)) AS var_perc_bad_docks,
    AVG(CAST(b.num_bikes_disabled AS DOUBLE) / CAST(COALESCE(b.capacity, 1) AS DOUBLE)) AS avg_perc_bad_bikes,
    VAR_POP(CAST(b.num_bikes_disabled AS DOUBLE) / CAST(COALESCE(b.capacity, 1) AS DOUBLE)) AS var_perc_bad_bikes,
    AVG(CAST(COALESCE(b.capacity, 1) AS DOUBLE)) AS avg_capacity
FROM (
    SELECT 
        rb.*,
        nm.short_id AS stationid,
        COALESCE(nm.capacity, 1) AS capacity,
        a.last_reported_nearest_hour,
        a.monthidx,
        a.weekday,
        a.shift
    FROM (
        SELECT 
            station_id,
            DATE_ADD(
                'hour',
                -5, -- Subtract 5 hours for timezone adjustment
                DATE_TRUNC('hour', FROM_UNIXTIME(last_reported))
            ) AS last_reported_nearest_hour,
            MONTH(
                DATE_ADD(
                    'hour',
                    -5,
                    DATE_TRUNC('hour', FROM_UNIXTIME(last_reported))
                )
            ) AS monthidx,
            DAY_OF_WEEK(
                DATE_ADD(
                    'hour',
                    -5,
                    DATE_TRUNC('hour', FROM_UNIXTIME(last_reported))
                )
            ) AS weekday,
            CASE
                WHEN HOUR(
                    DATE_ADD(
                        'hour',
                        -5,
                        DATE_TRUNC('hour', FROM_UNIXTIME(last_reported))
                    )
                ) BETWEEN 6 AND 9 THEN 1
                WHEN HOUR(
                    DATE_ADD(
                        'hour',
                        -5,
                        DATE_TRUNC('hour', FROM_UNIXTIME(last_reported))
                    )
                ) BETWEEN 10 AND 15 THEN 2
                WHEN HOUR(
                    DATE_ADD(
                        'hour',
                        -5,
                        DATE_TRUNC('hour', FROM_UNIXTIME(last_reported))
                    )
                ) BETWEEN 16 AND 19 THEN 3
                WHEN HOUR(
                    DATE_ADD(
                        'hour',
                        -5,
                        DATE_TRUNC('hour', FROM_UNIXTIME(last_reported))
                    )
                ) BETWEEN 19 AND 23 THEN 4
                ELSE 0
            END AS shift
        FROM rawbikes1
    ) AS a
    LEFT JOIN rawbikes1 AS rb
    ON rb.station_id = a.station_id
    LEFT JOIN num_map AS nm
    ON rb.station_id = nm.station_id
    WHERE rb.num_bikes_available IS NOT NULL AND COALESCE(nm.capacity, 1) > 0
) AS b
GROUP BY 
    b.stationid,
    b.monthidx,
    b.weekday,
    b.shift;
