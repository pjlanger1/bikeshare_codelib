CREATE EXTERNAL TABLE IF NOT EXISTS distances (
    origin STRING,
    destination STRING,
    distance FLOAT,
    angle FLOAT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
    'serialization.format' = ',',
    "skip.header.line.count" = "1"
)
STORED AS TEXTFILE
LOCATION 's3://cleanedcitibike/sim_dist'
TBLPROPERTIES ('has_encrypted_data'='false');
