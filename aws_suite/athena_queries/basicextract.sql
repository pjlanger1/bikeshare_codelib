/*Athena SQL lacks support for DISTINCT in SQL (the tables are initialized without keys on the backend)
  therefore, must take the circuitous route of window functions and a SELECT*.

  there isn't really a better way as far as i can tell.
  
  to do 10-21-24: port to databuildtool (dbt) 
**/
WITH ranked_rows AS (
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY station_id, last_reported ORDER BY station_id) AS rn
  FROM rawbikes
)
SELECT * 
FROM ranked_rows
WHERE rn = 1;
