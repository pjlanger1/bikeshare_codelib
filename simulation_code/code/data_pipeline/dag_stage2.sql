CREATE EXTERNAL TABLE IF NOT EXISTS distances (
origin string
destination string
distance float
angle float
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
    'serialization.format' = ','
) 
LOCATION 's3://cleanedcitibike/sim_dist'
TBLPROPERTIES ('has_encrypted_data'='false');
