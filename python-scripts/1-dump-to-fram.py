import argparse
import os
import csv

def process_txt_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_file_path = os.path.join(input_dir, filename)
            output_file_path = os.path.join(output_dir, filename.replace(".txt", ".csv"))
            
            with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
                csv_writer = csv.writer(outfile)
                csv_writer.writerow(["memory address", "data"])
                
                lines = infile.readlines()
                skip_next = False
                
                for i, line in enumerate(lines):
                    if "Frame ID: 011, Data: 02" in line:
                        parts = line.strip().split()
                        if len(parts) >= 8:
                            memory_address = parts[5] + parts[6]
                            data = ''.join(parts[-4:])
                            csv_writer.writerow([memory_address, data])
                    
                    elif "Data: 01" in line:
                        continue  # Skip this line as per requirement
                    
                    elif "Unknown" in line:
                        if i + 11 < len(lines) and all("Unknown" in lines[j] for j in range(i, i + 12)):
                            address_parts_1 = lines[i + 4].split()
                            address_parts_2 = lines[i + 5].split()
                            data_parts = [lines[i + j].split()[1] for j in range(7, 11)]

                            if len(address_parts_1) >= 2 and len(address_parts_2) >= 2 and len(data_parts) == 4:
                                address_parts_1[1] = address_parts_1[1].zfill(2)
                                address_parts_2[1] = address_parts_2[1].zfill(2)
                                for j in range(2, 6):
                                    data_parts[j - 2] = data_parts[j - 2].zfill(2)
                                memory_address = address_parts_1[1] + address_parts_2[1]
                                data = ''.join(data_parts)
                                csv_writer.writerow([memory_address, data])
                            skip_next = True
                    
                    elif skip_next:
                        skip_next = False  # Skip the remaining "Unknown" lines after processing
                        
if __name__ == "__main__":
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Convert text files to CSV format.")
    parser.add_argument("--input_dir", required=True, help="Path to the directory containing the input text files.")
    parser.add_argument("--output_dir", required=True, help="Path to the directory where the output CSV files will be saved.")

    args = parser.parse_args()

    # Create the output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    #input_directory = "path/to/your/txt/files"  # Change this to your actual directory
    #output_directory = "path/to/output/csv/files"  # Change this to where you want CSVs saved
    process_txt_files(args.input_dir, args.output_dir)
