import pandas as pd

def load_and_clean_data(csv_file):
    df = pd.read_csv(csv_file)

    # Standardize column names (lowercase)
    df.columns = [col.strip().lower() for col in df.columns]

    # Rename datetime column if needed
    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
    else:
        raise ValueError("❌ 'datetime' column not found in the CSV.")

    # Drop missing timestamps
    df = df.dropna(subset=['datetime'])

    # Time features
    df['hour'] = df['datetime'].dt.hour
    df['weekday'] = df['datetime'].dt.weekday
    df['month'] = df['datetime'].dt.month

    return df

def prepare_prophet_df(df):
    # Group by full datetime hour (not just hour of day)
    hourly = df.groupby(df['datetime'].dt.floor('H')).size().reset_index(name='ride_count')

    # Rename for Prophet
    hourly.rename(columns={'datetime': 'ds', 'ride_count': 'y'}, inplace=True)

    return hourly


