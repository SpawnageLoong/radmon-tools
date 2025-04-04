import os
import pandas as pd
import argparse

def load_temperature_data(temp_file_path):
    df = pd.read_csv(temp_file_path)
    df = df[['Date', 'Time', 'PV1', 'SP1']].copy()
    
    # Combine Date and Time into a datetime and filter out year 1970
    df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='coerce')
    df = df[df['datetime'].dt.year != 1970]
    
    df['Time'] = df['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df.rename(columns={'PV1': 'Temp Measured', 'SP1': 'Temp Setpoint'}, inplace=True)
    return df[['Time', 'Temp Measured', 'Temp Setpoint']]

def load_gm_data(input_dir):
    merged_gm_df = pd.DataFrame()

    for file in os.listdir(input_dir):
        if file.endswith(".csv") and "test-cycle-dump" in file:
            print(f"Loading GM data from {file}")
            file_path = os.path.join(input_dir, file)
            df = pd.read_csv(file_path)
            df = df.rename(columns={
                'time': 'Time',
                'gm tube count': 'GM Tube Count',
                'error count 1': 'Error Count #1',
                'error count 2': 'Error Count #2'
            })
            merged_gm_df = pd.concat([merged_gm_df, df], ignore_index=True)

    return merged_gm_df

def merge_data(temp_df, gm_df, start_time=None, end_time=None):
    # Convert Time to datetime
    temp_df['Time'] = pd.to_datetime(temp_df['Time'])
    gm_df['Time'] = pd.to_datetime(gm_df['Time'])

    # Filter by time range if provided
    if start_time:
        temp_df = temp_df[temp_df['Time'] >= start_time]
        gm_df = gm_df[gm_df['Time'] >= start_time]
    if end_time:
        temp_df = temp_df[temp_df['Time'] <= end_time]
        gm_df = gm_df[gm_df['Time'] <= end_time]

    # Merge on closest timestamps
    merged_df = pd.merge_asof(gm_df.sort_values('Time'),
                              temp_df.sort_values('Time'),
                              on='Time', direction='nearest')

    return merged_df[['Time', 'Temp Measured', 'Temp Setpoint', 'GM Tube Count', 'Error Count #1', 'Error Count #2']]

def run_merge(temp_file_path, gm_input_dir, output_path, start_time_str=None, end_time_str=None):
    start_time = pd.to_datetime(start_time_str) if start_time_str else None
    end_time = pd.to_datetime(end_time_str) if end_time_str else None

    temp_df = load_temperature_data(temp_file_path)
    gm_df = load_gm_data(gm_input_dir)
    merged_df = merge_data(temp_df, gm_df, start_time, end_time)
    merged_df.to_csv(output_path, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge temperature and GM tube count data.')
    parser.add_argument('--temp_csv', required=True, help='Path to the temperature CSV file')
    parser.add_argument('--input_dir', required=True, help='Path to directory with GM test-cycle-dump CSV files')
    parser.add_argument('--output_csv', required=True, help='Path to save the merged output CSV')
    parser.add_argument('--start_time', help='Start time in format YYYY-MM-DD HH:MM:SS', default=None)
    parser.add_argument('--end_time', help='End time in format YYYY-MM-DD HH:MM:SS', default=None)

    args = parser.parse_args()

    run_merge(args.temp_csv, args.input_dir, args.output_csv, args.start_time, args.end_time)
