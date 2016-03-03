import requests
import csv, time

base_url = 'https://api.instagram.com/v1'
ACCESS_TOKEN = 'Use your own'


f_image = open('instagramdataimages.csv','w')
f_video = open('instagramdatavideos.csv', 'w')

writer_image = csv.writer(f_image)
writer_video = csv.writer(f_video)

writer_image.writerow(['filter', 'comments', 'likes', 'latitude', 'longitude', 'locationname',\
		'locationid', 'createdtime', 'caption', 'imageurl', 'username', 'realname', 'id', 'link'])

writer_video.writerow(['filter', 'comments', 'likes', 'latitude', 'longitude', 'locationname',\
		'locationid', 'createdtime', 'caption', 'imageurl', 'username', 'realname', 'id', 'link'])


oscar_id = 1197608759160579970

for i in range(5000000):
	url = '{0}/media/{1}?access_token={2}'.format(base_url, str(i), ACCESS_TOKEN)
	r = requests.get(url)
	if r.status_code == 200:
		rjson = r.json()
		data = rjson['data']

		try:
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
			if data['type'] == 'image':
				writer_image.writerow([unicode(s).encode('utf-8') for s in row])
				print 'Got an image !!', (i)
			else:
				writer_video.writerow([unicode(s).encode('utf-8') for s in row])
				print 'Got a video !!', (i)
		except Exception as e:
			print e
	else:
		print 'ALARM! Not found'

	time.sleep(0.7)

f_image.close()
f_video.close()
