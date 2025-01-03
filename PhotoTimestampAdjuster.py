import os
import platform
from datetime import datetime

import pywintypes
import win32con
import win32file
from PIL import Image
from PIL.ExifTags import TAGS
from tqdm import tqdm


def get_exif_metadata(image_path):
    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()
            if exif_data is not None:
                return {TAGS.get(tag, tag): value for tag, value in exif_data.items()}
    except Exception as e:
        print(f"Error reading EXIF data from {image_path}: {e}")
    return {}


def changeFileCreationTime(fname, newtime):
    if platform.system() == "Windows":
        # os.utime(file_path, (new_creation_unixtime, modification_unixtime))
        # https://www.tutorialspoint.com/how-to-set-creation-and-modification-date-time-of-a-file-using-python

        wintime = pywintypes.Time(newtime)
        winfile = win32file.CreateFile(
            fname,
            win32con.GENERIC_WRITE,
            win32con.FILE_SHARE_READ
            | win32con.FILE_SHARE_WRITE
            | win32con.FILE_SHARE_DELETE,
            None,
            win32con.OPEN_EXISTING,
            win32con.FILE_ATTRIBUTE_NORMAL,
            None,
        )

        win32file.SetFileTime(winfile, wintime, None, None)

        winfile.close()
    else:
        print("Updating creation time not supported on this platform}")


def update_file_creation_date(file_path):
    stat = os.stat(file_path)

    # https://docs.python.org/3/library/stat.html
    modification_unixtime = stat.st_mtime
    creation_unixtime = stat.st_birthtime

    new_creation_unixtime = creation_unixtime

    if file_path.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")):
        exif_metadata = get_exif_metadata(file_path)
    else:
        exif_metadata = {}

    capture_date = exif_metadata.get("DateTime")

    # convert capture_date to unix timestamp
    if capture_date is not None:
        try:
            capture_date = datetime.strptime(capture_date, "%Y:%m:%d %H:%M:%S")
            capture_unix_time = capture_date.timestamp()
        except Exception as e:
            print(f"Error converting capture_date to unixtime for {file_path}: {e}")
            capture_unix_time = datetime.now().timestamp()

        new_creation_unixtime = min(
            creation_unixtime, modification_unixtime, capture_unix_time
        )
    else:
        new_creation_unixtime = min(creation_unixtime, modification_unixtime)

    # update only if date is not 1970-01-01 fake dates and lower than current creation date
    if new_creation_unixtime > 1 and new_creation_unixtime < creation_unixtime:
        try:
            # convert unix time to human readable format
            creation_humantime = datetime.fromtimestamp(creation_unixtime).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            new_creation_humantime = datetime.fromtimestamp(
                new_creation_unixtime
            ).strftime("%Y-%m-%d %H:%M:%S")
            print(
                f"Updated creation time from {creation_humantime} to {new_creation_humantime} for {file_path}"
            )

            # do change
            changeFileCreationTime(file_path, new_creation_unixtime)

        except Exception as e:
            print(f"Error updating creation time for {file_path}: {e}")
            # add to log file
            with open("error_log.txt", "a") as f:
                f.write(f"Error updating creation time for {file_path}: {e}\n")


def main(directory):
    # get all files in directory
    all_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            all_files.append(os.path.join(root, file))

    # add progress bar
    for file_path in tqdm(all_files, desc="Processing files", unit="file"):
        if file_path.endswith("Thumbs.db"):
            print(f"Suppress {file_path}")
            os.remove(file_path)
        else:
            update_file_creation_date(file_path)


if __name__ == "__main__":
    import sys

    directory = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    print(directory)
    main(directory)
