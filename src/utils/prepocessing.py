from typing import List

from analyzer.models import LogChunk
import pandas as pd


def log_chunk_preprocessor(logs_list: List[str]) -> LogChunk:

    df = pd.DataFrame(logs_list, columns=['log_entry'])

    # Extract the timestamp using regular expressions
    df['timestamp'] = df['log_entry'].str.extract(r'\[(.*?)\]')

    # Convert the timestamp into a datetime object, specifying the exact format
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%b/%Y:%H:%M:%S %z', errors='coerce')
    df.dropna(subset=['timestamp'], inplace=True)
    # Find the from-to time range
    from_time = df['timestamp'].min().isoformat()
    to_time = df['timestamp'].max().isoformat()

    return LogChunk(start_time=from_time, end_time=to_time, lines=logs_list)
