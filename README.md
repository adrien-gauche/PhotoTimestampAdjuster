# PhotoTimestampAdjuster

PhotoTimestampAdjuster is a Python script that updates the creation timestamps of image files based on their EXIF metadata. It ensures that the file creation date corresponds to the actual capture date (if available) or the earliest known modification date. The script also removes unwanted system files like `Thumbs.db`.

## Features
- Extracts EXIF metadata from image files to retrieve the capture date.
- Adjusts file creation timestamps based on the earliest known date.
- Processes all files recursively in a given directory.
- Automatically removes unnecessary files (e.g., `Thumbs.db`).
- Compatible with Windows platforms.

## Prerequisites
This script requires the following Python libraries:
- `os`
- `platform`
- `datetime`
- `pywin32`
- `Pillow` (PIL)
- `tqdm`

You can install the required libraries using pip:
```bash
pip install pywin32 pillow tqdm
```

## Usage

Run the script with the directory path containing the files you want to process. If no directory is specified, the script processes the current working directory.

```bash
python PhotoTimestampAdjuster.py [directory_path]
```

## Example:

```bash
python PhotoTimestampAdjuster.py "C:\Users\YourUsername\Pictures"
```


## How It Works

- Scans the directory (and subdirectories) for files.
- Extracts the EXIF metadata from supported image files (.png, .jpg, .jpeg, .tiff, .bmp, .gif).
- Adjusts the creation timestamp to match the capture date if available, or the earliest modification date otherwise.
- Logs any errors encountered in error_log.txt.

## Notes

- The script is designed to work on Windows systems, as it uses Windows-specific APIs for updating file timestamps.
- Updating the file creation time is not supported on non-Windows platforms.
- EXIF metadata must include the "DateTime" tag for capture date adjustments to work.

## Disclaimer

This script modifies file timestamps directly. Please ensure you have backups of your files before running the script.