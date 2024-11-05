CREATE EXTERNAL TABLE IF NOT EXISTS bikeshare_data (
    origin_station_id STRING,
    destination_station_id STRING,
    start_time TIMESTAMP,
    total_trips INT,
    ride_length FLOAT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpl
    'serialization.format' = ','
)
LOCATION 's3://your-bucket/path/to/bikeshare_data/'
TBLPROPERTIES ('has_encrypted_data'='false');
