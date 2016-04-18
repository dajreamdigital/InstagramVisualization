from flask import Flask, render_template,request,json
app = Flask(__name__,static_url_path='/static')

@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/visualize')
def visualize():
    return render_template('visualize.html')

@app.route('/recommend')
def recommend():

    result = ['vintage', 'lomo', 'clarity','sunrise']
    return json.dumps({"suggestions":result})

if __name__ == "__main__":
    app.run(debug=True)
