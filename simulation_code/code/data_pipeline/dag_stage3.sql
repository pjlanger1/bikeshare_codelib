CREATE EXTERNAL TABLE IF NOT EXISTS weather_data (
    time TIMESTAMP,
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
    dark INT,
    part_dark INT,
    light INT,
    holiday INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
LOCATION 's3://cleanedcitibike/weather_sim_data'
TBLPROPERTIES ('skip.header.line.count'='1');
