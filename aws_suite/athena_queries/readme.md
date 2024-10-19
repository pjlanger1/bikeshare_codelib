## query bank for the s3 buckets on transit ventures' tech stack.
primary keys:
*      ('station_id','last_reported')

fields: 
*       'station_id': 'string',
        'legacy_id': 'string', 
        'last_reported': 'long', 
        'num_bikes_available': int, 
        'num_bikes_disabled': int, 
        'num_ebikes_available': int, 
        'num_docks_available': int, 
        'num_docks_disabled': int, 
        'num_scooters_available': int, 
        'num_scooters_unavailable': int, 
        'is_renting': int, 
        'is_returning': int, 
        'is_installed': int

  Notes:
* when querying an s3 bucket containing raw historical data for research purposes, schema need to be formatted as such:
*      CREATE EXTERNAL TABLE IF NOT EXISTS rawbikes (
          station_id STRING,
          legacy_id STRING, 
          last_reported BIGINT, 
          num_bikes_available INT, 
          num_bikes_disabled INT, 
          num_ebikes_available INT, 
          num_docks_available INT, 
          num_docks_disabled INT, 
          num_scooters_available INT, 
          num_scooters_unavailable INT, 
          is_renting INT, 
          is_returning INT, 
          is_installed INT) 
        ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
        WITH SERDEPROPERTIES (
            "separatorChar" = ",",
            "quoteChar"     = "\""
            )
        LOCATION 's3://bucket/'
        TBLPROPERTIES ('skip.header.line.count'='0');

   * queries should do distinct on pairs of station_id and last_reported to enforce primary key:
       

