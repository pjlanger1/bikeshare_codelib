--arc flows
--input: od_distance_availability view


SELECT a.origin, a.destination, a.weekday, a.shift,
  AVG(s.total_trips) as a.mean_trips,
  AVG(s.mean_ride_len_seg) as a.mean_duration,
  AVG(s.distance) as s.mean_distance,
  AVG(s.angle) as s.mean_angle,
  AVG(s.origin_bikes_available)/ as ,
  AVG(s.origin_ebikes_available) as ,
  
  
  FROM a AS (
    SELECT origin, destination,
      CAST(DATE_FORMAT(start_time, '%w') AS INT) as weekday,
  
      CASE
        WHEN CAST(DATE_FORMAT(start_time, '%H') AS INT) BETWEEN 6 and 9 THEN 1
        WHEN CAST(DATE_FORMAT(start_time, '%H') AS INT) BETWEEN 10 and 15 THEN 2
        WHEN CAST(DATE_FORMAT(start_time, '%H') AS INT) BETWEEN 16 and 19 THEN 3
        WHEN CAST(DATE_FORMAT(start_time, '%H') AS INT) BETWEEN 19 and 23 THEN 4
        ELSE 0
      END AS shift,
      ride_length/total_trips as mean_ride_len_seg
      total_trips, ride_length, distance, angle, origin_bikes_available, origin_ebikes_available,
      origin_docks_available, origin_capacity, destination_docks_available, destination_capacity)

    GROUP BY a.origin, a.destination, a.weekday, a.shift
    
