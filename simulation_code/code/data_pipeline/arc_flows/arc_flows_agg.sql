-- Aggregating trips and availability data by origin-destination

SELECT 
    origin, 
    destination,
    -- Aggregated metrics
    AVG(total_trips) AS mean_trips,
    AVG(
        CASE 
            WHEN total_trips > 0 THEN ride_length / total_trips 
            ELSE NULL 
        END
    ) AS mean_duration,
    AVG(distance) AS mean_distance,
    AVG(angle) AS mean_angle,
    AVG(origin_bikes_available/origin_capacity) AS mean_origin_bike_cap,
    AVG(origin_ebikes_available/origin_capacity) AS mean_origin_ebike_cap,
    AVG(destination_docks_available/destination_capacity) AS mean_dest_dock_cap

FROM 
    od_distance_availability
GROUP BY
    origin, destination;
