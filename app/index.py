from flask import Flask, render_template,request,json
app = Flask(__name__,static_url_path='/static')

@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/visualize')
def visualize():
    return render_template('visualize.html')


# @app.route("/autocomplete")
# def autocomplete():
#     return render_template('autocomplete.html')
#
# @app.route('/ajaxautocomplete',methods=['POST', 'GET'])
# def ajaxautocomplete():
#     result=''
#     if request.method=='POST':
#      query=request.form['query']
#
#      try:
#
#       with connection.cursor() as cursor:
# 	      sql="select country_code data,country_name value from  countries where country_name like '%"+query+"%'"
# 	      cursor.execute(sql)
# 	      result = cursor.fetchall()
#      finally:
#       a=2
#      return json.dumps({"suggestions":result})
#     else:
#
#      return "ooops"


if __name__ == "__main__":
    app.run(debug=True)
