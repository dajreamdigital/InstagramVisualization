from flask import Flask, render_template,request,json
import requests
from object_detection import retrieve_class
import FilterRecommender

app = Flask(__name__,static_url_path='/static')

imageClass = None
createdTime = None
resultFilter = None

@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/visualize')
def visualize():
    return render_template('visualizeSeq.html')

@app.route('/instagram')
def instagram():
	return render_template('instagram.html')

@app.route('/getImage')
def getImage():
    base_url = 'https://api.instagram.com/v1'
    ACCESS_TOKEN = '3159841018.1fb234f.7184f0be946646bfb83fa32ca5c9cd7f'
    # ACCESS_TOKEN = '1312566635.1fb234f.4fecde8495fe4eeb8823ec21596f05b0 '
    # user = '1991460'
    try:
        #https://api.instagram.com/v1/users/self/media/recent/?access_token=ACCESS-TOKEN
        url = '{0}/users/self/media/recent?access_token={1}&count={2}'.format(base_url, ACCESS_TOKEN, 1)
        r = requests.get(url)
        if r.status_code == 200:
            rjson = r.json()
            urlImage = rjson['data'][0]['images']['low_resolution']['url']
            global createdTime
            global imageClass
            createdTime = rjson['data'][0]['created_time']
            imageClass = retrieve_class(urlImage)
            print imageClass
            print createdTime
            return json.dumps({'image' : urlImage, 'created_time' : createdTime})
			# time.sleep(2)
        else:
            return json.dumps({'status' : r.status_code})
    except Exception as ex:
        return json.dumps({'error' : ex})


@app.route('/recommend')
def recommend():
    global createdTime
    global imageClass
    global resultFilter
    param = [imageClass, createdTime]
    x = resultFilter.getRecommendations(param)
    print x
    # result = ['Clarendon', 'Ludwig', 'Lark','Juno']
    return json.dumps({"suggestions" : x.tolist(), "imageClass" : imageClass})

if __name__ == "__main__":
    global resultFilter
    resultFilter = FilterRecommender.FilterRecommender()
    app.run(debug=True)
