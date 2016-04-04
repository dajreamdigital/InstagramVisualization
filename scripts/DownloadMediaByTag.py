import requests, urllib
import csv, time

base_url = 'https://api.instagram.com/v1'
ACCESS_TOKEN = 'Use your own'

f_image = open('SelfieLinks.txt','w')

tag = 'selfie'
url = ''

for i in range(100):
	try:
		#url = ''
		if i == 0:
			url = '{0}/tags/{1}/media/recent?access_token={2}'.format(base_url, tag, ACCESS_TOKEN)
		print url
		r = requests.get(url)
		if r.status_code == 200:
			rjson = r.json()
			url = rjson['pagination']['next_url']
			print url
			datalist = rjson['data']
			print 'Got %d images in call %d'%(len(datalist),i)
			time.sleep(2)
			j = 0
			for data in datalist:
				try:
					imageurl = data['images']['standard_resolution']['url'].split('.jpg', 1)[0] + '.jpg'
					f_image.write(imageurl + '\n')
					urllib.urlretrieve(imageurl, "%d-%d.jpg"%(i,j))
					j += 1
				except Exception as e:
					print 'Error parsing image data'
					print e
		else:
			print 'Status code %d'%(r.status_code)
	except Exception as ex:
		print 'Error getting url'
		print ex

f_image.close()
