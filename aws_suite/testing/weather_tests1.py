import pandas as pd
def check_time_increments(df, date_column, start_date, end_date):
    """
    Checks if the DataFrame contains all 15-minute increments between two dates in a specified column.

    Args:
    df (pd.DataFrame): DataFrame containing the data.
    date_column (str): Name of the column containing the datetime values.
    start_date (str): Start date in 'YYYY-MM-DD HH:MM:SS' format.
    end_date (str): End date in 'YYYY-MM-DD HH:MM:SS' format.

    Returns:
    bool: True if all 15-minute increments are present, False otherwise.
    """
    
    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        df[date_column] = pd.to_datetime(df[date_column])

   
    expected_times = pd.date_range(start=start_date, end=end_date, freq='15T')

    actual_times = df[date_column].sort_values().unique()
    actual_times = pd.to_datetime(actual_times)
    missing_times = expected_times.difference(actual_times)
  
    if len(missing_times) == 0:
        return True
    else:
        print(f"Missing timestamps: {missing_times}")
        return False
