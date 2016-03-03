import requests
import csv, time

base_url = 'https://api.instagram.com/v1'
ACCESS_TOKEN = 'Use your own'


f = open('instagramdata.csv','w')

writer = csv.writer(f)
writer.writerow(['filter', 'comments', 'likes', 'latitude', 'longitude', 'locationname',\
		'locationid', 'createdtime', 'caption', 'imageurl', 'username', 'realname', 'id', 'link'])

for i in range(100000000):
	url = '{0}/media/{1}?access_token={2}'.format(base_url, str(i), ACCESS_TOKEN)
	r = requests.get(url)
	if r.status_code == 200:
		rjson = r.json()
		data = rjson['data']

		if data['type'] != 'image':
			continue

		row = [data['filter'], \
		data['comments']['count'],\
		data['likes']['count'],\
		data['location']['latitude'] if data['location'] else 'None',\
		data['location']['longitude'] if data['location'] else 'None',\
		data['location']['name'] if data['location'] else 'None',\
		data['location']['id'] if data['location'] else 'None',\
		data['created_time'],\
		data['caption'],\
		data['images']['standard_resolution']['url'],\
		data['user']['username'],\
		data['user']['full_name'],\
		data['id'],\
		data['link']]
		writer.writerow([unicode(s).encode('utf-8') for s in row])
	time.sleep(0.7)

f.close()