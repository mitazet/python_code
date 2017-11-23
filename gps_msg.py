import location
import notification
import requests
from time import sleep

geocode=location.get_location()
home_lat = geocode['latitude']
home_lng = geocode['longitude']
print(home_lat)
print(home_lng)

while True:
	sleep(20)
	location.start_updates()
	cur_geocode=location.get_location()
	cur_lat = cur_geocode['latitude']
	cur_lng = cur_geocode['longitude']
	print(home_lat)
	print(home_lng)
	if home_lat - 0.0003 < cur_lat and cur_lat < home_lat + 0.0003:
		if home_lng - 0.0003 < cur_lng and cur_lng < home_lng + 0.0003:
			payload = {'text': 'send_msg'}
			requests.post('http://192.168.10.110/', data=payload)
	
	location.stop_updates()
