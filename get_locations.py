import pandas as pd
import requests
from datetime import datetime
import json

# get coordinates
df = pd.read_csv('dogs_locations.csv')
coord = []
for i,r in df.iterrows():
	coord.append((r['latitude'],r['longitude']))

API_KEY = 'GET_YOUR_OWN_API_KEY'
URL = 'https://api.geocod.io/v1.6/reverse'
city_dict = {}
start = datetime.now()
#11211 coordinates
beg = 0
end = 2500
#stay within the free tier limit of 2500 daily API requests
for idx in range(beg,end):
	mycoord = str(coord[idx][0]) + ',' + str(coord[idx][1])
	PARAMS={'q':mycoord, 'api_key':API_KEY, 'limit':2}
	r = requests.get(url=URL,params=PARAMS)
	data = r.json()
	city = data['results'][0]['address_components']['city']
	state = data['results'][0]['address_components']['state']
	loc = city + ', ' + state
	print('Request # ',idx, "\t",loc)
	if loc not in city_dict.keys():
		city_dict[loc] = 0
	city_dict[loc]+=1
print('Elapsed time: ', datetime.now()-start)
cities_desc = [pair[0] for pair in sorted(city_dict.items(), key=lambda item: item[1])]
cities_desc.reverse()
print(cities_desc)
#output
outfile = 'cities_{b}_{e}.txt'.format(b=beg,e=end-1)
with open (outfile,'w') as f:
	json.dump(city_dict,f)
print('Output data written to ' + outfile)
