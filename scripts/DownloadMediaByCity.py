import requests
import csv, time

base_url = 'https://api.instagram.com/v1'
ACCESS_TOKEN = 'Use your own'

#Atlanta
lat = '38.907192'
lng = '-77.036871'

f_image = open('Washington.csv','w')

writer_image = csv.writer(f_image)

writer_image.writerow([ 'id', 'link', 'tags','filter', 'comments', 'likes', 'latitude', 'longitude',\
 'locationname', 'locationid', 'createdtime', 'imageurl', 'userid', 'username', 'realname'])

max_timestamp = int(time.time())
print max_timestamp

month_count = 0

for i in range(6000):
	try:
		url = '{0}/media/search?lat={1}&lng={2}&max_timestamp={3}&count=100&access_token={4}'.format(base_url, lat, lng, str(max_timestamp), ACCESS_TOKEN)
		r = requests.get(url)
		print url
		if r.status_code == 200:
            month_count = month_count + 1
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
                    data['user']['id'],\
					data['user']['username'],\
					data['user']['full_name'],\
					]
					if data['type'] == 'image':
						writer_image.writerow([unicode(s).encode('utf-8') for s in row])
				except Exception as e:
					print 'Error parsing image data'
					print e
			max_timestamp = datalist[-1]['created_time']
            if(month_count == 500):
                max_timestamp = max_timestamp - 2629743
                month_count = 0
			print 'max_timestamp is now ',max_timestamp
			time.sleep(1)
		else:
			print 'Status code %d'%(r.status_code)
	except Exception as ex:
		print 'Error getting url'
		print ex

	#time.sleep(0.7)

f_image.close()
