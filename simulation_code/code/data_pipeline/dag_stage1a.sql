CREATE TABLE bikeshare_data_cleaned
WITH (
    format = 'PARQUET',
    write_compression = 'SNAPPY'
) AS 
SELECT 
    origin_station_id,
    destination_station_id,
    CAST(start_time AS TIMESTAMP) AS start_time,
    total_trips,
    ride_length
FROM bikeshare_data
WHERE 
    REGEXP_LIKE(start_time, '^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$') 
    AND start_time IS NOT NULL;
