# radmon-tools
A set of programs for use in conjunction with the radmon-client to analyse logs and fram dumps.

## python-scripts

Both scripts have the same command format. They take an input directory and an output directory.


### 1-dump-to-fram.py

This script takes a directory of dump files (in txt format) and converts them to fram files (in csv format).
```
python3 1-dump-to-fram.py --input_dir <input_dir> --output_dir <output_dir>
```

### 2-fram-to-csv.py

This script takes a directory of fram files (in csv format) and converts them to human-readable data files (in csv format).
```
python3 2-fram-to-csv.py --input_dir <input_dir> --output_dir <output_dir>
```


### 3-merge-csv.py

This script takes a directory of human-readable data files (in csv format) and the thermal chamber data (in csv) and merges them into a single file. Start and end times can be specified to limit the data to a specific time range. Time should be in the format "YYYY-MM-DD HH:MM:SS".
```
python3 3-merge-csv.py --input_dir <input_dir> --output_csv <output_file> --temp_csv <temperature_file> --start_time <start_time> --end_time <end_time>
```
