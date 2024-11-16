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

  
