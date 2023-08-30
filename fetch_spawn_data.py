import requests
from utils import write_to_file
from env import API_URL

def main():
	if not API_URL:
		print("No API URL found! Please set D4_SCRAPE_API_URL environment variable.")
		return None

	response = requests.get(API_URL)
	response.raise_for_status()  # Raise an exception for HTTP errors
	data = response.json()

	write_to_file(data, "responses", "spawn_data")


if __name__ == "__main__":
	main()
