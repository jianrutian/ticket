# coding: utf-8

import json

with open('stations.json','r') as file:
	str = file.read()
	stations = json.loads(str)
	#print(type(stations))

def get_name(telecode):
	#print(stations.items())
	for name, code in stations.items():
		#print(name, code)
		if code == telecode:
			return name
	return None

def get_telecode(name):
    return stations[name]


#print(get_name('ZWQ'))

