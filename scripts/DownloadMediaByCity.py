import requests
import csv, time

base_url = 'https://api.instagram.com/v1'
ACCESS_TOKEN = 'Use your own'

#Atlanta
lat = '33.748995'
lng = '-84.387982'

f_image = open('Atlanta.csv','w')

writer_image = csv.writer(f_image)

writer_image.writerow([ 'id', 'link', 'tags','filter', 'comments', 'likes', 'latitude', 'longitude',\
 'locationname', 'locationid', 'createdtime', 'imageurl', 'username', 'realname'])

max_timestamp = int(time.time())
print max_timestamp

for i in range(5000):
	try:
		url = '{0}/media/search?lat={1}&lng={2}&max_timestamp={3}&count=100&access_token={4}'.format(base_url, lat, lng, str(max_timestamp), ACCESS_TOKEN)
		r = requests.get(url)
		print url
		if r.status_code == 200:
			rjson = r.json()
			datalist = rjson['data']
			print 'Got %d images in call %d'%(len(datalist), i)
			time.sleep(2)
			for data in datalist:
				try:
					row = [\
					data['id'],\
					data['link'],\
					data['tags'] if data['tags'] else 'None',\
					data['filter'], \
					data['comments']['count'],\
					data['likes']['count'],\
					data['location']['latitude'] if data['location'] else 'None',\
					data['location']['longitude'] if data['location'] else 'None',\
					data['location']['name'] if data['location'] else 'None',\
					data['location']['id'] if data['location'] else 'None',\
					data['created_time'],\
					data['images']['standard_resolution']['url'].split('.jpg', 1)[0] + '.jpg',\
					data['user']['username'],\
					data['user']['full_name'],\
					]
					if data['type'] == 'image':
						writer_image.writerow([unicode(s).encode('utf-8') for s in row])
				except Exception as e:
					print 'Error parsing image data'
					print e
			max_timestamp = datalist[-1]['created_time']
			print 'max_timestamp is now ',max_timestamp
			time.sleep(1)
		else:
			print 'Status code %d'%(r.status_code)
	except Exception as ex:
		print 'Error getting url'
		print ex
	
	#time.sleep(0.7)

f_image.close()
