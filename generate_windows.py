from datetime import datetime, timedelta
from repository import get_last_known_spawn_time, get_latest_spawn_estimates
from utils import date_format, write_to_file, time_to_timedelta


def is_within_time_window(time, windows):
	"""Check if a given time is within the defined time windows."""
	current_timedelta = time_to_timedelta(time.time())
	for window in windows:
		start, end = window
		# If the window spans over midnight, we'll handle that case by splitting into two intervals
		if start > end:
			# Check if the current time is within the first day's interval or the second day's interval
			if start <= current_timedelta or current_timedelta <= end:
				return True
		else:
			# For standard intervals where start is before end
			if start <= current_timedelta <= end:
				return True
	return False


def calculate_spawn_times(
	current_time,
	spawn_intervals,
	number_of_spawns,
	time_windows,
	interval_offset=0,
	future=True,
):
	"""
	Calculate spawn times based on a list of spawn intervals while considering time windows.
	"""
	spawns = []

	for i in range(number_of_spawns):
		if future:
			offset = (i + interval_offset) % len(spawn_intervals)
			current_time += spawn_intervals[offset]
		else:
			interval_offset -= 1  # decrementing the interval offset for past spawns
			offset = (interval_offset) % len(spawn_intervals)
			current_time -= spawn_intervals[offset]

		while not is_within_time_window(current_time, time_windows):
			current_time += timedelta(hours=2) if future else timedelta(hours=-2)

		spawns.append(
			{"time": current_time.strftime(date_format), "interval_offset": offset}
		)

	return spawns


def get_closest_interval(current_time, estimates):
	"""
	Determines which time in the estimates array is closest to the current_time.
	When the best match is found, return the interval.
	"""
	# Convert current_time to datetime if it's a string
	if isinstance(current_time, str):
		current_time = datetime.strptime(current_time, date_format)

	# Initialize minimum difference to a high value and interval to None
	min_diff = timedelta(days=365)  # Arbitrary large value
	closest_interval = None

	for entry in estimates:
		entry_time = datetime.strptime(entry["time"], date_format)
		diff = abs(entry_time - current_time)

		# Update the min_diff and closest_interval if current diff is smaller
		if diff < min_diff:
			min_diff = diff
			closest_interval = entry["interval_offset"]

	return closest_interval


def main():
	# Define the spawn intervals
	spawn_intervals = [
		timedelta(hours=5, minutes=53, seconds=30),
		timedelta(hours=5, minutes=25, seconds=13),
		timedelta(hours=5, minutes=53, seconds=29),
		timedelta(hours=5, minutes=53, seconds=30),
		timedelta(hours=5, minutes=25, seconds=13),
	]

	# Define the spawn time windows (converted from ET to UTC)
	time_windows = [
		(
			timedelta(hours=4, minutes=30),
			timedelta(hours=6, minutes=30),
		),  # Adjusting 00:30 - 02:30 ET to UTC
		(
			timedelta(hours=10, minutes=30),
			timedelta(hours=12, minutes=30),
		),  # Adjusting 06:30 - 08:30 ET to UTC
		(
			timedelta(hours=16, minutes=30),
			timedelta(hours=18, minutes=30),
		),  # Adjusting 12:30 - 14:30 ET to UTC
		(
			timedelta(hours=22, minutes=30),
			timedelta(hours=0, minutes=30),
		),  # Adjusting 18:30 - 20:30 ET to UTC
	]

	current_time = get_last_known_spawn_time()
	recent_estimates = get_latest_spawn_estimates()
	interval_offset = get_closest_interval(current_time, recent_estimates)

	spawn_count = 10

	# Calculate the previous 10 spawn times
	past_spawns = calculate_spawn_times(
		current_time, spawn_intervals, spawn_count, time_windows, interval_offset, future=False
	)
	# Reverse the list to show the oldest spawn first
	past_spawns.reverse()

	# Calculate the next 10 spawn times
	future_spawns = calculate_spawn_times(
		current_time,
		spawn_intervals,
		spawn_count,
		time_windows,
		interval_offset + 1,
		future=True,
	)

	current_spawn = [
		{
			"time": current_time.strftime(date_format),
			"interval_offset": interval_offset,
		}
	]

	# Compile spawns
	all_spawns = past_spawns + current_spawn + future_spawns

	write_to_file(all_spawns, "estimates", "estimate_data")


if __name__ == "__main__":
	main()
