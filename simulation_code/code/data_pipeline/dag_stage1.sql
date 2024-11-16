CREATE EXTERNAL TABLE IF NOT EXISTS bikeshare_data (
    origin_station_id STRING,
    destination_station_id STRING,
    start_time TIMESTAMP,
    total_trips INT,
    ride_length FLOAT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    "separatorChar" = ",",
    "quoteChar"     = "\"",
    "skip.header.line.count" = "1"
)
LOCATION 's3://cleanedcitibike/sim_read_data'
TBLPROPERTIES ('has_encrypted_data'='false');
