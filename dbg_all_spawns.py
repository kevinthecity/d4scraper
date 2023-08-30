from datetime import datetime
from dateutil import tz
from repository import get_latest_spawn_estimates

def utc_to_local(utc_dt):
    """Converts a UTC datetime object to a local datetime object based on the system's local timezone."""
    local_zone = tz.tzlocal()
    local_dt = utc_dt.astimezone(local_zone)
    return local_dt

def main():
    estimates = get_latest_spawn_estimates()
    current_utc_time = datetime.utcnow().replace(tzinfo=tz.tzutc())

    # Filter the estimates to only those that are after (or equal to) the current time.
    future_spawns = [e for e in estimates if datetime.fromisoformat(e['time']) >= current_utc_time]
    
    # Convert and print each UTC time in the future_spawns to the system's local time zone
    for estimate in future_spawns:
        utc_time = datetime.fromisoformat(estimate['time']).replace(tzinfo=tz.tzutc())
        local_time = utc_to_local(utc_time)
        print(local_time.strftime('%m/%d/%y %H:%M'))

if __name__ == "__main__":
    main()
