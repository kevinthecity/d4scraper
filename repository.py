from datetime import datetime
import json

from utils import get_latest_file


# Function to get spawn time from a file
def get_spawn_time_from_file(filename):
    with open(filename, "r") as file:
        data = json.load(file)
        return datetime.utcfromtimestamp(data["previousEvent"]["time"] / 1000)


def get_last_known_spawn_time():
    # Check spawn time from the most recent file
    latest_file = get_latest_file("responses")
    if latest_file:
        return get_spawn_time_from_file(latest_file)
    else:
        return None


def get_latest_spawn_estimates():
    # Check spawn time from the most recent file
    latest_file = get_latest_file("estimates")
    if latest_file:
        with open(latest_file, "r") as file:
            return json.load(file)
    else:
        return None
