from datetime import datetime
from repository import get_latest_spawn_estimates
from utils import date_format, write_to_file

current_utc_time = datetime.utcnow()

def next_spawn_time():
	estimates = get_latest_spawn_estimates()
	if not estimates:
		print("None returned from get_latest_spawn_estimates()")
		return None
	
	# Filter the estimates to only those that are after (or equal to) the current time.
	future_spawns = [e for e in estimates if datetime.strptime(e['time'], date_format) >= current_utc_time]
	
	if not future_spawns:
		print("No future spawns found!")
		return None

	# Get the first future spawn
	first_future_spawn = datetime.strptime(future_spawns[0]['time'], date_format) 
	return first_future_spawn

def main():
	spawn_time = next_spawn_time()
	if not spawn_time:
		print("No spawn time found!")
		return None

	output_data = {
		"boss_name": 'D4 Boss',
		"spawn_time": spawn_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
		"request_time": current_utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')
	}
	
	write_to_file(output_data, 'spawns', 'spawn_data')

if __name__ == '__main__':
	main()