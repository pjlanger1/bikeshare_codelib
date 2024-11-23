CREATE EXTERNAL TABLE IF NOT EXISTS weather_data (
    time STRING,
    max_temp FLOAT,
    min_temp FLOAT,
    temp FLOAT,
    wind_chill FLOAT,
    heat_index FLOAT,
    precip FLOAT,
    snow FLOAT,
    snow_depth FLOAT,
    wind_speed FLOAT,
    wind_direction FLOAT,
    wind_gust FLOAT,
    visibility FLOAT,
    cloud_cover FLOAT,
    humid FLOAT,
    clear_cond INT,
    none_cond FLOAT,
    overcast_cond INT,
    partially_cloudy_cond INT,
    rain_cond INT,
    snow_cond FLOAT,
    month_sin FLOAT,
    month_cos FLOAT,
    day_sin FLOAT,
    day_cos FLOAT,
    hour_sin FLOAT,
    hour_cos FLOAT,
    minute_sin FLOAT,
    minute_cos FLOAT,
    day_of_week_sin FLOAT,
    day_of_week_cos FLOAT,
    dark INT,
    part_dark INT,
    light INT,
    holiday INT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
    'serialization.format' = ',',
    "skip.header.line.count" = "1"
) 
LOCATION 's3://cleanedcitibike/weather_sim_data'
TBLPROPERTIES ('has_encrypted_data'='false');
