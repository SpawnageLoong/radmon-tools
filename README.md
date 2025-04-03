# radmon-tools
A set of programs for use in conjunction with the radmon-client to analyse logs and fram dumps.

## python-scripts

Both scripts have the same command format. They take an input directory and an output directory.
```
python3 script.py <input_dir> <output_dir>
```

### 1-dump-to-fram.py

This script takes a directory of dump files (in txt format) and converts them to fram files (in csv format).

### 2-fram-to-csv.py

This script takes a directory of fram files (in csv format) and converts them to human-readable data files (in csv format).