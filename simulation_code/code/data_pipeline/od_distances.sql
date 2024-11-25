CREATE TABLE od_distance_availability AS
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
    rb_origin.capacity AS origin_capacity,
    
    -- Destination station availability metrics
    rb_dest.num_docks_available AS destination_docks_available,
    rb_dest.capacity AS destination_capacity,
    rb_dest.num_bikes_available AS destination_bikes_available  -- Optional for dockless scenarios
FROM 
    bikeshare_data_cleaned AS bs
JOIN 
    distances AS d
ON 
    bs.origin_station_id = d.origin
    AND bs.destination_station_id = d.destination
LEFT JOIN 
    rawbikes AS rb_origin
ON 
    bs.origin_station_id = rb_origin.short_id
    -- If last_reported_nearest_hour is a string, convert it to TIMESTAMP
    AND bs.start_time = rb_origin.last_reported_nearest_hour
LEFT JOIN 
    rawbikes AS rb_dest
ON 
    bs.destination_station_id = rb_dest.short_id
    -- If last_reported_nearest_hour is a string, convert it to TIMESTAMP
    AND bs.start_time = rb_dest.last_reported_nearest_hour;
