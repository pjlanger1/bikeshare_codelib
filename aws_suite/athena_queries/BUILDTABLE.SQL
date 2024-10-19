CREATE EXTERNAL TABLE IF NOT EXISTS rawbikes (
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
  LOCATION 's3://bucket'
  TBLPROPERTIES ('skip.header.line.count'='0');
