from flask import Flask, render_template,request,json
import requests

app = Flask(__name__,static_url_path='/static')

@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/visualize')
def visualize():
    return render_template('visualize_it.html')

@app.route('/instagram')
def instagram():
	return render_template('instagram.html')

@app.route('/getImage')
def getImage():
	base_url = 'https://api.instagram.com/v1'
	ACCESS_TOKEN = '3159841018.1fb234f.7184f0be946646bfb83fa32ca5c9cd7f'
	user = '1991460'	
	try:
		#https://api.instagram.com/v1/users/self/media/recent/?access_token=ACCESS-TOKEN
		url = '{0}/users/self/media/recent?access_token={1}&count={2}'.format(base_url, ACCESS_TOKEN, 1)
		r = requests.get(url)
		if r.status_code == 200:
			rjson = r.json()
			image_url = rjson['data'][0]['images']['low_resolution']['url']
			created_time = rjson['data'][0]['created_time']
			print image_url
			print created_time
			return json.dumps({'image' : image_url, 'created_time' : created_time})
			time.sleep(2)
		else:
			return json.dumps({'status' : r.status_code})
	except Exception as ex:
		return json.dumps({'error' : ex})


@app.route('/recommend')
def recommend():
    result = ['vintage', 'lomo', 'clarity','sunrise']
    return json.dumps({"suggestions" : result})
if __name__ == "__main__":
    app.run(debug=True)
