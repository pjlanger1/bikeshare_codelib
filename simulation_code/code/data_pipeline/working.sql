CREATE EXTERNAL TABLE IF NOT EXISTS rawbikes1 (
    station_id STRING,
    legacy_id STRING, 
    last_reported BIGINT, 
    num_bikes_available INT, 
    num_bikes_disabled INT, 
    num_ebikes_available INT, 
    num_docks_available INT, 
    num_docks_disabled INT, 
    num_scooters_available INT, 
    num_scooters_unavailable INT, 
    is_renting INT, 
    is_returning INT, 
    is_installed INT) 
  ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
  WITH SERDEPROPERTIES (
      "separatorChar" = ",",
      "quoteChar"     = "\""
      )
  LOCATION 's3://jsonpublicfeed/'
  TBLPROPERTIES ('skip.header.line.count'='0');

--next
  
  CREATE TABLE rawbikes AS
SELECT * 
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY station_id, last_reported ORDER BY station_id) AS rn
    FROM rawbikes1
) ranked_rows
WHERE rn = 1;


--last
  SELECT 
    bs.origin_station_id AS origin,
    bs.destination_station_id AS destination,
    bs.start_time,
    bs.total_trips,
    bs.ride_length,
    d.distance,
    d.angle,
    
    -- Origin station availability metrics
    rb_origin.num_bikes_available AS origin_bikes_available,
    rb_origin.num_ebikes_available AS origin_ebikes_available,
    rb_origin.num_docks_available AS origin_docks_available,
    
    -- Destination station availability metrics
    rb_dest.num_docks_available AS destination_docks_available,
    rb_dest.num_bikes_available AS destination_bikes_available  -- Optional for dockless scenarios

FROM 
    bikeshare_data AS bs
JOIN 
    distances AS d
ON 
    bs.origin_station_id = d.origin
    AND bs.destination_station_id = d.destination
LEFT JOIN 
    rawbikes AS rb_origin
ON 
    bs.origin_station_id = rb_origin.station_id
    AND bs.start_time = FROM_UNIXTIME(rb_origin.last_reported)
LEFT JOIN 
    rawbikes AS rb_dest
ON 
    bs.destination_station_id = rb_dest.station_id
    AND bs.start_time = FROM_UNIXTIME(rb_dest.last_reported);



-- now this is the second to last

, base_flows AS (
    SELECT 
        origin,
        destination,
        CAST(DATE_FORMAT(start_time, '%w') AS INT) AS day_of_week,
        
        -- Define time of day segments
        CASE
            WHEN CAST(DATE_FORMAT(start_time, '%H') AS INT) BETWEEN 6 AND 9 THEN 'morning'
            WHEN CAST(DATE_FORMAT(start_time, '%H') AS INT) BETWEEN 10 AND 15 THEN 'afternoon'
            WHEN CAST(DATE_FORMAT(start_time, '%H') AS INT) BETWEEN 16 AND 19 THEN 'evening'
            WHEN CAST(DATE_FORMAT(start_time, '%H') AS INT) BETWEEN 20 AND 23 THEN 'night'
            ELSE 'early_morning'
        END AS time_of_day,
        
        -- Aggregate trip and availability metrics
        SUM(total_trips) AS total_trips,                     -- Total trips for each segment
        AVG(total_trips) AS avg_trip_count,                  -- Average trips for each segment
        AVG(ride_length) AS avg_ride_length,                 -- Average ride length
        AVG(distance) AS avg_distance,                       -- Average distance for each segment
        AVG(angle) AS avg_angle,                             -- Average angle (optional for spatial analysis)
        AVG(origin_bikes_available) AS avg_origin_bikes,     -- Average bikes available at origin
        AVG(origin_docks_available) AS avg_origin_docks,     -- Average docks available at origin
        AVG(destination_bikes_available) AS avg_dest_bikes,  -- Average bikes available at destination
        AVG(destination_docks_available) AS avg_dest_docks   -- Average docks available at destination
        
    FROM 
        od_distance_availability
    GROUP BY 
        origin, 
        destination, 
        CAST(DATE_FORMAT(start_time, '%w') AS INT),     -- Day of week (0 = Sunday, 6 = Saturday)
        CASE
            WHEN CAST(DATE_FORMAT(start_time, '%H') AS INT) BETWEEN 6 AND 9 THEN 'morning'
            WHEN CAST(DATE_FORMAT(start_time, '%H') AS INT) BETWEEN 10 AND 15 THEN 'afternoon'
            WHEN CAST(DATE_FORMAT(start_time, '%H') AS INT) BETWEEN 16 AND 19 THEN 'evening'
            WHEN CAST(DATE_FORMAT(start_time, '%H') AS INT) BETWEEN 20 AND 23 THEN 'night'
            ELSE 'early_morning'
        END
)


--and this is the last

SELECT 
    bf.origin,
    bf.destination,
    bf.day_of_week,
    bf.time_of_day,
    bf.avg_trip_count,
    bf.total_trips,
    bf.avg_ride_length,
    bf.avg_distance,
    bf.avg_angle,
    bf.avg_origin_bikes,
    bf.avg_origin_docks,
    bf.avg_dest_bikes,
    bf.avg_dest_docks,
    
    -- Weather metrics as additional exogenous variables
    w.temp AS temperature,
    w.precip AS precipitation,
    w.wind_speed AS wind_speed,
    w.cloud_cover AS cloud_cover,
    w.humid AS humidity,
    
    -- Sine and cosine cyclic encoding for month, day, and time
    w.month_sin, 
    w.month_cos, 
    w.day_of_week_sin, 
    w.day_of_week_cos,
    w.hour_sin,
    w.hour_cos
    
FROM 
    base_flows AS bf
JOIN 
    weather_data AS w
ON 
    bf.time_of_day = CASE
        WHEN CAST(DATE_FORMAT(w.time, '%H') AS INT) BETWEEN 6 AND 9 THEN 'morning'
        WHEN CAST(DATE_FORMAT(w.time, '%H') AS INT) BETWEEN 10 AND 15 THEN 'afternoon'
        WHEN CAST(DATE_FORMAT(w.time, '%H') AS INT) BETWEEN 16 AND 19 THEN 'evening'
        WHEN CAST(DATE_FORMAT(w.time, '%H') AS INT) BETWEEN 20 AND 23 THEN 'night'
        ELSE 'early_morning'
    END
    AND bf.day_of_week = CAST(DATE_FORMAT(w.time, '%w') AS INT)
ORDER BY 
    bf.origin, 
    bf.destination, 
    bf.day_of_week, 
    bf.time_of_day;


  
