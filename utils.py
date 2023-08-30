import os
from datetime import timedelta, datetime
import json
import glob

date_format = "%Y-%m-%dT%H:%M:%SZ"

def write_to_file(data, dir_name, file_name):
    filename = get_timestamped_json_filename(dir_name, file_name)
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {filename}")


def get_current_time_string():
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")


def get_timestamped_json_filename(dir_name, file_name):
    filename = get_file_path(dir_name, f"{file_name}_{get_current_time_string()}.json")
    return filename


def get_file_path(dir_name, file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dir_path = os.path.join(script_dir, dir_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    file_path = os.path.join(dir_path, file_name)
    return file_path


def get_latest_file(folder):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(script_dir, folder)

    list_of_files = glob.glob(os.path.join(folder_path, "*"))
    if not list_of_files:
        return None
    return max(list_of_files, key=os.path.getctime)


def time_to_timedelta(t):
    """Convert a datetime.time to datetime.timedelta."""
    return timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
