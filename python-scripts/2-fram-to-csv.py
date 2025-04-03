import argparse
import os
import csv
from datetime import datetime

def hex_to_dec(hex_str):
    return int(hex_str, 16)

def hex_to_unix_timestamp(hex_str):
    return datetime.utcfromtimestamp(int(hex_str, 16)).strftime('%Y-%m-%d %H:%M:%S')

def process_csv_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            input_file_path = os.path.join(input_dir, filename)
            output_file_path = os.path.join(output_dir, filename.replace(".csv", "_processed.csv"))
            
            with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
                csv_reader = csv.reader(infile)
                csv_writer = csv.writer(outfile)
                
                next(csv_reader)  # Skip header row
                csv_writer.writerow(["time", "gm tube count", "error count 1", "error count 2"])
                
                rows = list(csv_reader)
                
                for i in range(0, len(rows), 105):
                    if i + 2 < len(rows):
                        time_hex = rows[i][1]  # First row's data field
                        gm_count_hex = rows[i+1][1]  # Second row's data field
                        error_hex = rows[i+2][1]  # Third row's data field
                        
                        time_str = hex_to_unix_timestamp(time_hex)
                        gm_count = hex_to_dec(gm_count_hex)
                        error_count_1 = hex_to_dec(error_hex[:4])
                        error_count_2 = hex_to_dec(error_hex[4:])
                        
                        csv_writer.writerow([time_str, gm_count, error_count_1, error_count_2])
                        
if __name__ == "__main__":
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Convert text files to CSV format.")
    parser.add_argument("input_dir", help="Path to the directory containing the input text files.")
    parser.add_argument("output_dir", help="Path to the directory where the output CSV files will be saved.")

    args = parser.parse_args()

    # Create the output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    #input_directory = "path/to/your/csv/files"  # Change to your actual input directory
    #output_directory = "path/to/output/csv/files"  # Change to where you want processed CSVs saved
    process_csv_files(args.input_dir, args.output_dir)
