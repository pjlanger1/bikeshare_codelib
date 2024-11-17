CREATE TABLE rawbikes AS
SELECT * 
FROM (
    SELECT *,
           DATE_ADD(
               'hour', 
               CASE 
                   WHEN CAST(DATE_FORMAT(FROM_UNIXTIME(last_reported), '%i') AS INT) >= 30 THEN 1
                   ELSE 0 
               END, -- Add 1 hour if minutes >= 30
               DATE_TRUNC('hour', FROM_UNIXTIME(last_reported))
           ) AS last_reported_nearest_hour, -- Round to nearest hour
           ROW_NUMBER() OVER (PARTITION BY station_id, last_reported ORDER BY station_id) AS rn
    FROM rawbikes1
) ranked_rows
WHERE rn = 1;
